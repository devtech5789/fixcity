from attachments.models import Attachment
from django.conf import settings
from django.contrib import comments
from django.contrib.contenttypes.models import ContentType
from django.contrib.sites.models import Site
from django.utils.encoding import smart_unicode
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.platypus import Image
from reportlab.platypus import PageBreak
from reportlab.platypus import Paragraph
from reportlab.platypus import SimpleDocTemplate
from reportlab.platypus import Spacer
from reportlab.platypus import Table
from reportlab.platypus import TableStyle
from voting.models import Vote
import datetime
import os

import logging

logger = logging.getLogger()

stylesheet = getSampleStyleSheet()
normalStyle = stylesheet['Normal']

# TODO: this massively needs caching!

Comment = comments.get_model()

def make_pdf(bulk_order, outfile):
    """
    Generates a PDF and writes it to file-like object `outfile`.
    """
    logger.info('Starting make_pdf')
    cb = bulk_order.communityboard
    doc = SimpleDocTemplate(outfile, pagesize=letter,
                            leftMargin=0.5 * inch,
                            rightMargin=0.75 * inch,
                            )

    # XXX Sorting by street would be nice, but we don't have
    # addresses split into components, so we can't.
    racks = sorted(bulk_order.racks, key=lambda x: x.date)

    body = []

    body.append(Paragraph('Bike Rack Bulk Order:\n%s' % str(cb),
                          stylesheet['h1']))
    body.append(make_rack_table(racks))

    for rack in racks:
        body.append(PageBreak())
        body.extend(make_rack_page(rack))

    doc.build(body)
    logger.info('Finished make_pdf')


def make_rack_table(racks):
    header = ['No.', 'Address', 'Date', 'Establishment',
              'Email', 'Verified?', 'Source']
    header = [Paragraph('<b>%s</b>' % s, normalStyle) for s in header]
    rows = [header]
    
    for rack in racks:
        verified = rack.verified and 'Y' or 'N'
        rows.append([str(rack.id),
                     Paragraph(rack.address, normalStyle),
                     rack.date.date(),
                     Paragraph(rack.title, normalStyle),
                     rack.email, verified, rack.source or 'web'])

    rack_listing = Table(rows, 
                         colWidths=[25, 100, 55, 100, 120, 45, 40],
                         repeatRows=1)
    rack_listing.setStyle(TableStyle(
            [('ROWBACKGROUNDS', (0, 1), (-1, -1),
              [colors.white, colors.Color(0.9, 0.91, 0.96)],
              ),
             ('VALIGN', (0, 1), (-1, -1), 'TOP'),
             ]))
    return rack_listing


def make_rack_page(rack):
    # I suppose we 'should' use a PageTemplate and Frames and so
    # forth, but frankly I don't have enough time to learn Platypus
    # well enough to understand them.
    flowables = []
    flowables.append(Paragraph('%s. %s' % (rack.id, rack.title),
                               stylesheet['h1']))
    flowables.append(Paragraph(rack.address, stylesheet['h1']))
    from fixcity.bmabr.views import cross_streets_for_rack

    prev_street, next_street = cross_streets_for_rack(rack)
    prev_street = str(prev_street).title()
    next_street = str(next_street).title()
    flowables.append(Paragraph(
            'Cross Streets: %s and %s' % (prev_street, next_street),
            stylesheet['h2']))

    # Make a map image.
    # Derive the bounding box from rack center longitude/latitude.
    # The offset was arrived at empirically by guess-and-adjust.
    ratio = 0.65
    x_offset = 0.002
    y_offset = x_offset * ratio
    bounds = (rack.location.x - x_offset, rack.location.y - y_offset,
              rack.location.x + x_offset, rack.location.y + y_offset)
 
    image_pixels_x = 640  # That's the most google will give us.
    image_pixels_y = image_pixels_x * ratio

    image_inches_x = 3.5 * inch
    image_inches_y = image_inches_x * ratio

    tries = 3
    for i in range(tries):
        try:
            the_map = get_map(bounds, size=(image_pixels_x, image_pixels_y),
                              format='jpg')
            break
        except RuntimeError:
            if i == tries -1:
                raise
            else:
                continue
    
    map_row = [Image(the_map, width=image_inches_x, height=image_inches_y)]

    # Photo, if provided.
    if rack.photo.name:
        photo = rack.photo.extra_thumbnails['large']
        map_row.append(Image(photo.dest, width=image_inches_x,
                              )) #height=image_inches_y))
    else:
        map_row.append(Paragraph('<i>no photo provided</i>', normalStyle))

    map_table = Table([map_row], colWidths=[image_inches_x + 0.25,
                                            image_inches_x + 0.25],
                                                
                      style=TableStyle([
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                ]))



    flowables.append(map_table)
    flowables.append(Spacer(0, 0.25 * inch))
  
    flowables.append(Paragraph('Description', stylesheet['h1']))
    flowables.append(Paragraph(rack.description or 'none', normalStyle))

    votes = Vote.objects.get_score(rack)
    flowables.append(Spacer(0, 0.25 * inch))
    flowables.append(Paragraph('<b>%d likes</b>' % votes['score'], normalStyle))

    comment_count = Comment.objects.filter(
        content_type=ContentType.objects.get_for_model(rack),
        object_pk=smart_unicode(rack.pk), site__pk=settings.SITE_ID).count()

    flowables.append(Paragraph('<b>%d comments</b>' % comment_count, normalStyle))
    # TODO: append comment text!

    return flowables



def get_map(bbox, size=(400, 256), format='jpg'):
    """Generate a map given some bounding box.  Writes the image to file
    and returns the filename.  ReportLab reads the image given a filename
    during doc.build.  This file should be deleted after the doc is built.
    Perhaps this will be different with a PIL image.

    XXX would be nice to use our own tiles, but this was already working
    """
    # Originally copied from the old Almanac grok code,
    # http://svn.opengeo.org/almanac/siteapp/trunk/opengeo/almanac/pdf.py

    import urllib, httplib2, tempfile

    # GMap API Key for opengeo.org - static api doesn't care about origin
    url = 'http://maps.google.com/staticmap'
    key = settings.GOOGLE_MAPS_KEY

    center = ((bbox[2] + bbox[0]) / 2, (bbox[3] + bbox[1]) / 2)
    span = (bbox[2] - bbox[0], bbox[3] - bbox[1])
    
    params = {'center': '%f,%f' % (center[1], center[0]),
              'span': '%f,%f' % (span[1], span[0]),
              'size': '%dx%d' % (size[0], size[1]),
              'format': format,
              'key': key}    
    query = urllib.urlencode(params)
    url = "%s?%s" % (url, query)
    logger.debug('Fetching %r' % url )
    http = httplib2.Http('.cache', timeout=30)
    # Google has some sort of rate limit, but they don't document what it is.
    # (Also a daily cap of 1000 per client.)
    # Let's sleep a bit and pray...
    import time
    time.sleep(1)
    response, data = http.request(url)
    if response.status != 200:
        raise RuntimeError("Response %s while retrieving %s" % (response.status, url))
    # would be nice to deal directly with image data instead of writing first
    # XXX this means we need a cron job or similar to clean up old files in $TMP
    tmp, path = tempfile.mkstemp('.%s' % format)
    os.write(tmp, data)
    os.close(tmp)

    return path

def make_csv(bo, outfile):
    logger.info('Start make_csv')
    import csv
    fieldnames = ("ID", "TrackNum", "DateIn", "Action_", "GenBy",
                  "Requestor", "Address", "Address2", "ReqBoro", "ZipCode",
                  "Phone", "Email", "Title", "RComment",
                  "LocName", "LocAdd", "LocAddNum", 
                  "Street", "From_", "To_",
                  "Width", "x", "y", "Boro", "LocZip",
                  "CB", "Comments", "Area", "SubStation", "SubLine",
                  "Status", "Sited", "SitedBy", "InspDate", "InspBy",
                  "Side", "Sm", "Lg", "RackType",
                  "MeterNum", "DOTRespDat", "CBNoteDate", "CommNote",
                  "WorkOrder", "InstDate", "Invoice", "Image_", "txtImgName")

    # In python 2.7 you can do: csv_writer.writeheader()
    outfile.write(', '.join(fieldnames))
    outfile.write('\r\n')

    csv_writer = csv.DictWriter(outfile, fieldnames)

    from fixcity.bmabr.views import cross_streets_for_rack, neighborhood_for_rack
    from fixcity.bmabr.models import CommunityBoard
    from fixcity.bmabr.models import StatementOfSupport
    for rack in bo.racks:
        from_st, to_st = cross_streets_for_rack(rack)
        neighborhood = neighborhood_for_rack(rack)
        cb = CommunityBoard.objects.get(the_geom__intersects=rack.location)
        try:
            site_domain = Site.objects.get_current().domain
            photo_url = 'http://%s%s' % (site_domain, rack.photo.url)
        except (ValueError, AttributeError):
            photo_url = ''
        row = {
            "ID": '', 'TrackNum': '',
            'DateIn':  rack.date.strftime('%m/%d/%Y'),
            'Action_': 'REQUEST',
            'GenBy': 'INTERNET',  #rack.source or 'web',
            'Requestor': rack.user or rack.email,
            'Address': '', 'Address2': '',  # user's address?
            'ReqBoro': cb.borough.boroname,  # user's or rack's?? actually should be a 2-letter code but we just have names.
            'ZipCode': '',
            'Phone': '',
            'Email': rack.email,
            'Title': '',  # eg. Dr, Mr, Mrs ...
            'RComment': rack.description,
            'LocName': rack.title,
            'LocAdd': '',  # Number part of rack address?
            'LocAddNum': '',  # Number part of rack address again?
            'Street': rack.address,  # Should be just the street part?
            'From_': from_st,
            'To_': to_st,
            'Width': '',  # what's this?
            'x': '',  # maybe a longitude? but in some other units?
            'y': '',  # maybe a latitude? but what are the units??
            'Boro': cb.borough.borocode,  # or what? should be '1' for manhattan??
            'LocZip': '',  # rack's zip? don't have it.
            'CB': cb.borocd,
            'Comments':  '',  # for DOT's internal use?
            'Area': neighborhood,
            'SubStation': '',  # subway station
            'SubLine': '',   # subway line
            'Status': 'P',  #  always submit as 'Pending'.
            # DOT internal statuses: "sited" (approved for install),
            # "rejected" (with a comment), "installed" (DOT has
            # audited it post-install)
            'Sited': '', 'SitedBy': '',  # only if installed.
            'InspDate': '', 'InspBy': '',
            'Side': '', 'Sm': '', 'Lg': '', 'RackType': '',
            'MeterNum': '', 'DOTRespDat': '', 'CBNoteDate': '',
            'CommNote': '', 'WorkOrder': '', 'InstDate': '',
            'Invoice': '',
            'Image_': '', 
            'txtImgName': photo_url,  # URL ok here?
            }

        statement_query = StatementOfSupport.objects.filter(s_rack=rack.id)
        for s in statement_query:
            # What to do with these? DOT doesn't really have a place for them.
            #row.append(s.file.url)
            pass

        # DictWriter doesn't handle encoding automatically.
        for k, v in row.items():
            if v is None:
                v = u''
            if isinstance(v, basestring):
                row[k] = v.encode('utf8')
        csv_writer.writerow(row)
    logger.info('Start make_csv')

def make_zip(bulk_order, outfile):
    """Generates a zip and writes it to file-like object `outfile`.
    """
    logger.info('Start make_zip')
    now = datetime.datetime.utcnow().timetuple()[:6]
    import zipfile
    zf = zipfile.ZipFile(outfile, 'w')
    from cStringIO import StringIO
    pdf = StringIO()
    make_pdf(bulk_order, pdf)
    name = make_filename(bulk_order, 'pdf')
    info = zipfile.ZipInfo(name, date_time=now)
    # Workaround for permissions bug, see http://bugs.python.org/issue3394
    info.external_attr = 0660 << 16L
    zf.writestr(info, pdf.getvalue())

    csv = StringIO()
    make_csv(bulk_order, csv)
    name = make_filename(bulk_order, 'csv')
    info = zipfile.ZipInfo(name, date_time=now)
    info.external_attr = 0660 << 16L
    zf.writestr(info, csv.getvalue())

    for attachment in Attachment.objects.attachments_for_object(bulk_order):
        path = attachment.attachment_file.path
        info = zipfile.ZipInfo(os.path.basename(path), date_time=now)
        info.external_attr = 0660 << 16L
        # Rats. We have files on disk already so I'd like to use zf.write(),
        # but you can't call that when output is a stringio instance
        # because zf.write() apparently needs to call seek().
        zf.writestr(info, open(path).read())

    zf.close()
    logger.info('Finished make_zip')



def make_filename(bulk_order, extension):
    """
    Make a filename based on the bulk_order's metadata and the
    provided extension.
    """
    # TODO: DOT wants a unique ID number on each BO request
    # as part of the filename;
    # re-submitting would change the number.
    # so if eg. they forward the files around they know which is which.
    # Maybe the timestamp is enough?
    date = bulk_order.date.replace(microsecond=0)
    cb = bulk_order.communityboard
    name = "%s_%s.%s" % (str(cb).replace(' ', '-'), date.isoformat('-'),
                         extension)
    name = name.replace(':', '')
    return name


