# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'User.age'
        db.add_column('contest_user', 'age',
                      self.gf('django.db.models.fields.IntegerField')(null=True),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'User.age'
        db.delete_column('contest_user', 'age')


    models = {
        'contest.contest': {
            'Meta': {'object_name': 'Contest'},
            'admin': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contest.User']"}),
            'date_created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'date_submission_closed': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'date_voting_closed': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '64'})
        },
        'contest.submission': {
            'Meta': {'object_name': 'Submission'},
            'author': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contest.User']"}),
            'date_created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'sc_url': ('django.db.models.fields.URLField', [], {'max_length': '200'})
        },
        'contest.user': {
            'Meta': {'object_name': 'User'},
            'age': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'date_created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '64'})
        },
        'contest.vote': {
            'Meta': {'object_name': 'Vote'},
            'date_created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'score': ('django.db.models.fields.IntegerField', [], {}),
            'submission': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contest.Submission']"}),
            'voter': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contest.User']"})
        }
    }

    complete_apps = ['contest']