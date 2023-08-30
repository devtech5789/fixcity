# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'CommunityBoard'
        db.create_table(u'gis_community_board', (
            ('gid', self.gf('django.db.models.fields.IntegerField')(primary_key=True)),
            ('borocd', self.gf('django.db.models.fields.IntegerField')()),
            ('board', self.gf('django.db.models.fields.IntegerField')()),
            ('borough', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['bmabr.Borough'])),
            ('the_geom', self.gf('django.contrib.gis.db.models.fields.MultiPolygonField')()),
        ))
        db.send_create_signal('bmabr', ['CommunityBoard'])

        # Adding model 'Rack'
        db.create_table('bmabr_rack', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('address', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=140)),
            ('date', self.gf('django.db.models.fields.DateTimeField')()),
            ('description', self.gf('django.db.models.fields.CharField')(max_length=300, blank=True)),
            ('email', self.gf('django.db.models.fields.EmailField')(max_length=75, blank=True)),
            ('photo', self.gf('django.db.models.fields.files.ImageField')(max_length=100, null=True, blank=True)),
            ('user', self.gf('django.db.models.fields.CharField')(max_length=20, blank=True)),
            ('location', self.gf('django.contrib.gis.db.models.fields.PointField')()),
            ('verify_surface', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('verify_objects', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('verify_access', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('status', self.gf('django.db.models.fields.CharField')(default='new', max_length=20, blank=True)),
            ('source', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['bmabr.Source'], null=True, blank=True)),
        ))
        db.send_create_signal('bmabr', ['Rack'])

        # Adding M2M table for field bulk_orders on 'Rack'
        db.create_table('bmabr_rack_bulk_orders', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('rack', models.ForeignKey(orm['bmabr.rack'], null=False)),
            ('nycdotbulkorder', models.ForeignKey(orm['bmabr.nycdotbulkorder'], null=False))
        ))
        db.create_unique('bmabr_rack_bulk_orders', ['rack_id', 'nycdotbulkorder_id'])

        # Adding model 'Source'
        db.create_table('bmabr_source', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=20)),
        ))
        db.send_create_signal('bmabr', ['Source'])

        # Adding model 'EmailSource'
        db.create_table('bmabr_emailsource', (
            ('source_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['bmabr.Source'], unique=True, primary_key=True)),
            ('address', self.gf('django.db.models.fields.EmailField')(max_length=75)),
        ))
        db.send_create_signal('bmabr', ['EmailSource'])

        # Adding model 'TwitterSource'
        db.create_table('bmabr_twittersource', (
            ('source_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['bmabr.Source'], unique=True, primary_key=True)),
            ('user', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('status_id', self.gf('django.db.models.fields.CharField')(max_length=32)),
        ))
        db.send_create_signal('bmabr', ['TwitterSource'])

        # Adding model 'SeeClickFixSource'
        db.create_table('bmabr_seeclickfixsource', (
            ('source_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['bmabr.Source'], unique=True, primary_key=True)),
            ('issue_id', self.gf('django.db.models.fields.IntegerField')()),
            ('reporter', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('image_url', self.gf('django.db.models.fields.URLField')(max_length=200)),
        ))
        db.send_create_signal('bmabr', ['SeeClickFixSource'])

        # Adding model 'StatementOfSupport'
        db.create_table('bmabr_statementofsupport', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('file', self.gf('django.db.models.fields.files.FileField')(max_length=100, null=True, blank=True)),
            ('email', self.gf('django.db.models.fields.EmailField')(max_length=75)),
            ('s_rack', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['bmabr.Rack'])),
        ))
        db.send_create_signal('bmabr', ['StatementOfSupport'])

        # Adding model 'Neighborhood'
        db.create_table(u'gis_neighborhoods', (
            ('gid', self.gf('django.db.models.fields.IntegerField')(primary_key=True)),
            ('objectid', self.gf('django.db.models.fields.IntegerField')()),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('borough', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('city', self.gf('django.db.models.fields.CharField')(default='New York City', max_length=50)),
            ('state', self.gf('django.db.models.fields.CharField')(default='NY', max_length=2, null=True)),
            ('the_geom', self.gf('django.contrib.gis.db.models.fields.PointField')()),
        ))
        db.send_create_signal('bmabr', ['Neighborhood'])

        # Adding model 'Borough'
        db.create_table(u'gis_boroughs', (
            ('gid', self.gf('django.db.models.fields.IntegerField')(primary_key=True)),
            ('borocode', self.gf('django.db.models.fields.SmallIntegerField')()),
            ('boroname', self.gf('django.db.models.fields.CharField')(max_length=32)),
            ('shape_leng', self.gf('django.db.models.fields.DecimalField')(max_digits=1000, decimal_places=100)),
            ('shape_area', self.gf('django.db.models.fields.DecimalField')(max_digits=1000, decimal_places=100)),
            ('the_geom', self.gf('django.contrib.gis.db.models.fields.MultiPolygonField')()),
        ))
        db.send_create_signal('bmabr', ['Borough'])

        # Adding model 'CityRack'
        db.create_table(u'gis_cityracks', (
            ('gid', self.gf('django.db.models.fields.IntegerField')(primary_key=True)),
            ('objectid', self.gf('django.db.models.fields.DecimalField')(max_digits=1000, decimal_places=100)),
            ('address', self.gf('django.db.models.fields.DecimalField')(max_digits=1000, decimal_places=100)),
            ('street_nam', self.gf('django.db.models.fields.CharField')(max_length=31)),
            ('zip_code_1', self.gf('django.db.models.fields.CharField')(max_length=12, null=True)),
            ('from__cros', self.gf('django.db.models.fields.CharField')(max_length=22)),
            ('to__cross', self.gf('django.db.models.fields.CharField')(max_length=22, null=True)),
            ('boro_1', self.gf('django.db.models.fields.CharField')(max_length=8)),
            ('neighborho', self.gf('django.db.models.fields.CharField')(max_length=21, null=True)),
            ('side_of_st', self.gf('django.db.models.fields.CharField')(max_length=12, null=True)),
            ('small', self.gf('django.db.models.fields.IntegerField')()),
            ('large', self.gf('django.db.models.fields.IntegerField')()),
            ('alt_addres', self.gf('django.db.models.fields.CharField')(max_length=31, null=True)),
            ('x', self.gf('django.db.models.fields.DecimalField')(max_digits=1000, decimal_places=100)),
            ('y', self.gf('django.db.models.fields.DecimalField')(max_digits=1000, decimal_places=100)),
            ('id', self.gf('django.db.models.fields.CharField')(max_length=13, null=True)),
            ('oppaddress', self.gf('django.db.models.fields.DecimalField')(max_digits=1000, decimal_places=100)),
            ('borocode', self.gf('django.db.models.fields.DecimalField')(max_digits=1000, decimal_places=100)),
            ('c_racksid', self.gf('django.db.models.fields.CharField')(max_length=17)),
            ('rackid', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('the_geom', self.gf('django.contrib.gis.db.models.fields.PointField')()),
        ))
        db.send_create_signal('bmabr', ['CityRack'])

        # Adding model 'NYCDOTBulkOrder'
        db.create_table('bmabr_nycdotbulkorder', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('communityboard', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['bmabr.CommunityBoard'])),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('date', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('organization', self.gf('django.db.models.fields.CharField')(max_length=128, null=True)),
            ('rationale', self.gf('django.db.models.fields.TextField')(null=True)),
            ('status', self.gf('django.db.models.fields.CharField')(default='new', max_length=32, blank=True)),
        ))
        db.send_create_signal('bmabr', ['NYCDOTBulkOrder'])

        # Adding model 'NYCStreet'
        db.create_table(u'gis_nycstreets', (
            ('gid', self.gf('django.db.models.fields.IntegerField')(primary_key=True)),
            ('street', self.gf('django.db.models.fields.CharField')(max_length=35)),
            ('nodeidfrom', self.gf('django.db.models.fields.CharField')(max_length=7)),
            ('nodeidto', self.gf('django.db.models.fields.CharField')(max_length=7)),
            ('zipleft', self.gf('django.db.models.fields.CharField')(max_length=5, null=True)),
            ('the_geom', self.gf('django.contrib.gis.db.models.fields.MultiLineStringField')()),
        ))
        db.send_create_signal('bmabr', ['NYCStreet'])


    def backwards(self, orm):
        
        # Deleting model 'CommunityBoard'
        db.delete_table(u'gis_community_board')

        # Deleting model 'Rack'
        db.delete_table('bmabr_rack')

        # Removing M2M table for field bulk_orders on 'Rack'
        db.delete_table('bmabr_rack_bulk_orders')

        # Deleting model 'Source'
        db.delete_table('bmabr_source')

        # Deleting model 'EmailSource'
        db.delete_table('bmabr_emailsource')

        # Deleting model 'TwitterSource'
        db.delete_table('bmabr_twittersource')

        # Deleting model 'SeeClickFixSource'
        db.delete_table('bmabr_seeclickfixsource')

        # Deleting model 'StatementOfSupport'
        db.delete_table('bmabr_statementofsupport')

        # Deleting model 'Neighborhood'
        db.delete_table(u'gis_neighborhoods')

        # Deleting model 'Borough'
        db.delete_table(u'gis_boroughs')

        # Deleting model 'CityRack'
        db.delete_table(u'gis_cityracks')

        # Deleting model 'NYCDOTBulkOrder'
        db.delete_table('bmabr_nycdotbulkorder')

        # Deleting model 'NYCStreet'
        db.delete_table(u'gis_nycstreets')


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
            'zipleft': ('django.db.models.fields.CharField', [], {'max_length': '5', 'null': 'True'})
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
