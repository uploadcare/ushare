# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Changing field 'ImageFile.date_created'
        db.alter_column('files_imagefile', 'date_created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, null=True))

        # Changing field 'ImageFile.file'
        db.alter_column('files_imagefile', 'file', self.gf('pyuploadcare.dj.models.FileField')(null=True))

    def backwards(self, orm):

        # User chose to not deal with backwards NULL issues for 'ImageFile.date_created'
        raise RuntimeError("Cannot reverse this migration. 'ImageFile.date_created' and its values cannot be restored.")

        # User chose to not deal with backwards NULL issues for 'ImageFile.file'
        raise RuntimeError("Cannot reverse this migration. 'ImageFile.file' and its values cannot be restored.")

    models = {
        'files.imagefile': {
            'Meta': {'object_name': 'ImageFile'},
            'date_created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'null': 'True', 'blank': 'True'}),
            'file': ('pyuploadcare.dj.models.FileField', [], {'null': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        }
    }

    complete_apps = ['files']