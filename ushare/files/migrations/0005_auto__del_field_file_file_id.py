# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting field 'File.file_id'
        db.delete_column('files_file', 'file_id')


    def backwards(self, orm):
        # Adding field 'File.file_id'
        db.add_column('files_file', 'file_id',
                      self.gf('django.db.models.fields.TextField')(default=u''),
                      keep_default=False)


    models = {
        'files.file': {
            'Meta': {'object_name': 'File'},
            'date_created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'null': 'True', 'blank': 'True'}),
            'file_obj': ('pyuploadcare.dj.models.FileField', [], {'null': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        }
    }

    complete_apps = ['files']