# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting model 'ImageFile'
        db.delete_table('files_imagefile')

        # Adding model 'File'
        db.create_table('files_file', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('file_obj', self.gf('pyuploadcare.dj.models.FileField')(null=True)),
            ('file_id', self.gf('django.db.models.fields.TextField')(default=u'')),
            ('date_created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, null=True, blank=True)),
        ))
        db.send_create_signal('files', ['File'])


    def backwards(self, orm):
        # Adding model 'ImageFile'
        db.create_table('files_imagefile', (
            ('date_created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, null=True, blank=True)),
            ('file_id', self.gf('django.db.models.fields.TextField')(default=u'')),
            ('file', self.gf('pyuploadcare.dj.models.FileField')(null=True)),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal('files', ['ImageFile'])

        # Deleting model 'File'
        db.delete_table('files_file')


    models = {
        'files.file': {
            'Meta': {'object_name': 'File'},
            'date_created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'null': 'True', 'blank': 'True'}),
            'file_id': ('django.db.models.fields.TextField', [], {'default': "u''"}),
            'file_obj': ('pyuploadcare.dj.models.FileField', [], {'null': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        }
    }

    complete_apps = ['files']