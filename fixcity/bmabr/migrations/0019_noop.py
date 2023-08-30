# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        pass
        # # Adding model 'NYCStreet'
        # sql_path = os.path.abspath(
        #     os.path.join(HERE, '..', '..', 'data', 'shps', 'nyc_streets',
        #                  'gis_nycstreets.sql.gz'))
        # import gzip
        # z = gzip.GzipFile(sql_path)
        # db.execute_many(z.read())
        # db.send_create_signal('bmabr', ['NYCStreet'])


    def backwards(self, orm):
        pass
        # # Deleting model 'NYCStreet'
        # db.delete_table(u'gis_nycstreets')


    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'ordering': "('content_type__app_label', 'content_type__model', 'codename')", 'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'bmabr.borough': {
            'Meta': {'object_name': 'Borough', 'db_table': "u'gis_boroughs'"},
            'borocode': ('django.db.models.fields.SmallIntegerField', [], {}),
            'boroname': ('django.db.models.fields.CharField', [], {'max_length': '32'}),
            'gid': ('django.db.models.fields.IntegerField', [], {'primary_key': 'True'}),
            'shape_area': ('django.db.models.fields.DecimalField', [], {'max_digits': '1000', 'decimal_places': '100'}),
            'shape_leng': ('django.db.models.fields.DecimalField', [], {'max_digits': '1000', 'decimal_places': '100'}),
            'the_geom': ('django.contrib.gis.db.models.fields.MultiPolygonField', [], {})
        },
        'bmabr.cityrack': {
            'Meta': {'object_name': 'CityRack', 'db_table': "u'gis_cityracks'"},
            'address': ('django.db.models.fields.DecimalField', [], {'max_digits': '1000', 'decimal_places': '100'}),
            'alt_addres': ('django.db.models.fields.CharField', [], {'max_length': '31', 'null': 'True'}),
            'boro_1': ('django.db.models.fields.CharField', [], {'max_length': '8'}),
            'borocode': ('django.db.models.fields.DecimalField', [], {'max_digits': '1000', 'decimal_places': '100'}),
            'c_racksid': ('django.db.models.fields.CharField', [], {'max_length': '17'}),
            'from__cros': ('django.db.models.fields.CharField', [], {'max_length': '22'}),
            'gid': ('django.db.models.fields.IntegerField', [], {'primary_key': 'True'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '13', 'null': 'True'}),
            'large': ('django.db.models.fields.IntegerField', [], {}),
            'neighborho': ('django.db.models.fields.CharField', [], {'max_length': '21', 'null': 'True'}),
            'objectid': ('django.db.models.fields.DecimalField', [], {'max_digits': '1000', 'decimal_places': '100'}),
            'oppaddress': ('django.db.models.fields.DecimalField', [], {'max_digits': '1000', 'decimal_places': '100'}),
            'rackid': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'side_of_st': ('django.db.models.fields.CharField', [], {'max_length': '12', 'null': 'True'}),
            'small': ('django.db.models.fields.IntegerField', [], {}),
            'street_nam': ('django.db.models.fields.CharField', [], {'max_length': '31'}),
            'the_geom': ('django.contrib.gis.db.models.fields.PointField', [], {}),
            'to__cross': ('django.db.models.fields.CharField', [], {'max_length': '22', 'null': 'True'}),
            'x': ('django.db.models.fields.DecimalField', [], {'max_digits': '1000', 'decimal_places': '100'}),
            'y': ('django.db.models.fields.DecimalField', [], {'max_digits': '1000', 'decimal_places': '100'}),
            'zip_code_1': ('django.db.models.fields.CharField', [], {'max_length': '12', 'null': 'True'})
        },
        'bmabr.communityboard': {
            'Meta': {'ordering': "['board']", 'object_name': 'CommunityBoard', 'db_table': "u'gis_community_board'"},
            'board': ('django.db.models.fields.IntegerField', [], {}),
            'borocd': ('django.db.models.fields.IntegerField', [], {}),
            'borough': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['bmabr.Borough']"}),
            'gid': ('django.db.models.fields.IntegerField', [], {'primary_key': 'True'}),
            'the_geom': ('django.contrib.gis.db.models.fields.MultiPolygonField', [], {})
        },
        'bmabr.emailsource': {
            'Meta': {'object_name': 'EmailSource', '_ormbases': ['bmabr.Source']},
            'address': ('django.db.models.fields.EmailField', [], {'max_length': '75'}),
            'source_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['bmabr.Source']", 'unique': 'True', 'primary_key': 'True'})
        },
        'bmabr.neighborhood': {
            'Meta': {'object_name': 'Neighborhood', 'db_table': "u'gis_neighborhoods'"},
            'borough': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'city': ('django.db.models.fields.CharField', [], {'default': "'New York City'", 'max_length': '50'}),
            'gid': ('django.db.models.fields.IntegerField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'objectid': ('django.db.models.fields.IntegerField', [], {}),
            'state': ('django.db.models.fields.CharField', [], {'default': "'NY'", 'max_length': '2', 'null': 'True'}),
            'the_geom': ('django.contrib.gis.db.models.fields.PointField', [], {})
        },
        'bmabr.nycdotbulkorder': {
            'Meta': {'object_name': 'NYCDOTBulkOrder'},
            'communityboard': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['bmabr.CommunityBoard']"}),
            'date': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'organization': ('django.db.models.fields.CharField', [], {'max_length': '128', 'null': 'True'}),
            'rationale': ('django.db.models.fields.TextField', [], {'null': 'True'}),
            'status': ('django.db.models.fields.CharField', [], {'default': "'new'", 'max_length': '32', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"})
        },
        'bmabr.nycstreet': {
            'Meta': {'object_name': 'NYCStreet', 'db_table': "u'gis_nycstreets'"},
            'gid': ('django.db.models.fields.IntegerField', [], {'primary_key': 'True'}),
            'nodeidfrom': ('django.db.models.fields.CharField', [], {'max_length': '7'}),
            'nodeidto': ('django.db.models.fields.CharField', [], {'max_length': '7'}),
            'street': ('django.db.models.fields.CharField', [], {'max_length': '35'}),
            'the_geom': ('django.contrib.gis.db.models.fields.MultiLineStringField', [], {}),
            'zipleft': ('django.db.models.fields.CharField', [], {'max_length': '5'})
        },
        'bmabr.rack': {
            'Meta': {'object_name': 'Rack'},
            'address': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'bulk_orders': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['bmabr.NYCDOTBulkOrder']", 'null': 'True', 'blank': 'True'}),
            'date': ('django.db.models.fields.DateTimeField', [], {}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '300', 'blank': 'True'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'location': ('django.contrib.gis.db.models.fields.PointField', [], {}),
            'photo': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'source': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['bmabr.Source']", 'null': 'True', 'blank': 'True'}),
            'status': ('django.db.models.fields.CharField', [], {'default': "'new'", 'max_length': '20', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '140'}),
            'user': ('django.db.models.fields.CharField', [], {'max_length': '20', 'blank': 'True'}),
            'verify_access': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'verify_objects': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'verify_surface': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        'bmabr.seeclickfixsource': {
            'Meta': {'object_name': 'SeeClickFixSource', '_ormbases': ['bmabr.Source']},
            'image_url': ('django.db.models.fields.URLField', [], {'max_length': '200'}),
            'issue_id': ('django.db.models.fields.IntegerField', [], {}),
            'reporter': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'source_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['bmabr.Source']", 'unique': 'True', 'primary_key': 'True'})
        },
        'bmabr.source': {
            'Meta': {'object_name': 'Source'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '20'})
        },
        'bmabr.statementofsupport': {
            'Meta': {'ordering': "['s_rack']", 'object_name': 'StatementOfSupport'},
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75'}),
            'file': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            's_rack': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['bmabr.Rack']"})
        },
        'bmabr.twittersource': {
            'Meta': {'object_name': 'TwitterSource', '_ormbases': ['bmabr.Source']},
            'source_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['bmabr.Source']", 'unique': 'True', 'primary_key': 'True'}),
            'status_id': ('django.db.models.fields.CharField', [], {'max_length': '32'}),
            'user': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        }
    }

    complete_apps = ['bmabr']
