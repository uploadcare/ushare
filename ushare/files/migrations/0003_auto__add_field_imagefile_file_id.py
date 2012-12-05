# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'ImageFile.file_id'
        db.add_column('files_imagefile', 'file_id',
                      self.gf('django.db.models.fields.TextField')(default=u''),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'ImageFile.file_id'
        db.delete_column('files_imagefile', 'file_id')


    models = {
        'files.imagefile': {
            'Meta': {'object_name': 'ImageFile'},
            'date_created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'null': 'True', 'blank': 'True'}),
            'file': ('pyuploadcare.dj.models.FileField', [], {'null': 'True'}),
            'file_id': ('django.db.models.fields.TextField', [], {'default': "u''"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        }
    }

    complete_apps = ['files']