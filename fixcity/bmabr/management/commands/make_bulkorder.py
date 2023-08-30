
from django.conf import settings
from django.core.management.base import BaseCommand
import optparse

logger = settings.LOGGER

class Command(BaseCommand):
    option_list = BaseCommand.option_list + (
    )

    def handle(self, *args, **options):
        if len(args) < 2:
            raise optparse.OptParseError("Need a borough name and a community board number")

        logger.debug('starting handle')
        from fixcity.bmabr.models import NYCDOTBulkOrder
        from fixcity.bmabr.models import CommunityBoard
        from django.contrib.auth.models import User

        # What user? Ugh, hardcode this for now.
        try:
            user = User.objects.get(username='admin')
        except User.DoesNotExist:
            user = User.objects.filter(is_superuser=True)[0] # ugh!!!

        borough, cb_number = args[0], int(args[1])
        cb = CommunityBoard.objects.get(borough__boroname=borough,
                                        board=cb_number)
        bulk_order, created = NYCDOTBulkOrder.objects.get_or_create(
            communityboard=cb, user=user, organization='OpenPlans',
            rationale='just testing')
        logger.info('Creating new bulk order' if created
                    else"Existing bulk order")
        bulk_order.approve()
        bulk_order.save()

        from fixcity.bmabr import bulkorder
        filename = bulkorder.make_filename(bulk_order, 'zip')
        outfile = open(filename, 'w')
        bulkorder.make_zip(bulk_order, outfile)
        outfile.close()
        logger.info( "Output written to %s" % filename)
        # Stashing this here so tests can clean up... ugh.
        self._filename = filename

