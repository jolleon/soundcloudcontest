# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Changing field 'Contest.date_submission_closed'
        db.alter_column('contest_contest', 'date_submission_closed', self.gf('django.db.models.fields.DateTimeField')(null=True))

        # Changing field 'Contest.date_voting_closed'
        db.alter_column('contest_contest', 'date_voting_closed', self.gf('django.db.models.fields.DateTimeField')(null=True))

    def backwards(self, orm):

        # Changing field 'Contest.date_submission_closed'
        db.alter_column('contest_contest', 'date_submission_closed', self.gf('django.db.models.fields.DateTimeField')(default=None))

        # Changing field 'Contest.date_voting_closed'
        db.alter_column('contest_contest', 'date_voting_closed', self.gf('django.db.models.fields.DateTimeField')(default=None))

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