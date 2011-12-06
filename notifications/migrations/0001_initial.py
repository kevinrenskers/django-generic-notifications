# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'NotificationQueue'
        db.create_table('notifications_notificationqueue', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(related_name='notifications', to=orm['auth.User'])),
            ('subject', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('text', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('tries', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
            ('notification_backend', self.gf('django.db.models.fields.CharField')(max_length=255)),
        ))
        db.send_create_signal('notifications', ['NotificationQueue'])

        # Adding model 'SelectedNotificationsType'
        db.create_table('notifications_selectednotificationstype', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('notification_type', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('notification_backends', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal('notifications', ['SelectedNotificationsType'])

        # Adding unique constraint on 'SelectedNotificationsType', fields ['user', 'notification_type']
        db.create_unique('notifications_selectednotificationstype', ['user_id', 'notification_type'])

        # Adding model 'NotificationBackendSettings'
        db.create_table('notifications_notificationbackendsettings', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('notification_backend', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('settings', self.gf('django.db.models.fields.TextField')(default='{}')),
        ))
        db.send_create_signal('notifications', ['NotificationBackendSettings'])

        # Adding unique constraint on 'NotificationBackendSettings', fields ['user', 'notification_backend']
        db.create_unique('notifications_notificationbackendsettings', ['user_id', 'notification_backend'])


    def backwards(self, orm):
        
        # Removing unique constraint on 'NotificationBackendSettings', fields ['user', 'notification_backend']
        db.delete_unique('notifications_notificationbackendsettings', ['user_id', 'notification_backend'])

        # Removing unique constraint on 'SelectedNotificationsType', fields ['user', 'notification_type']
        db.delete_unique('notifications_selectednotificationstype', ['user_id', 'notification_type'])

        # Deleting model 'NotificationQueue'
        db.delete_table('notifications_notificationqueue')

        # Deleting model 'SelectedNotificationsType'
        db.delete_table('notifications_selectednotificationstype')

        # Deleting model 'NotificationBackendSettings'
        db.delete_table('notifications_notificationbackendsettings')


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
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'unique': 'True', 'null': 'True'}),
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
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'notifications.notificationbackendsettings': {
            'Meta': {'unique_together': "(['user', 'notification_backend'],)", 'object_name': 'NotificationBackendSettings'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'notification_backend': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'settings': ('django.db.models.fields.TextField', [], {'default': "'{}'"}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"})
        },
        'notifications.notificationqueue': {
            'Meta': {'object_name': 'NotificationQueue'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'notification_backend': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'subject': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'text': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'tries': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'notifications'", 'to': "orm['auth.User']"})
        },
        'notifications.selectednotificationstype': {
            'Meta': {'unique_together': "(['user', 'notification_type'],)", 'object_name': 'SelectedNotificationsType'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'notification_backends': ('django.db.models.fields.TextField', [], {}),
            'notification_type': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"})
        }
    }

    complete_apps = ['notifications']
