# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'User'
        db.create_table('contest_user', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=64)),
            ('date_created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal('contest', ['User'])

        # Adding model 'Contest'
        db.create_table('contest_contest', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=64)),
            ('description', self.gf('django.db.models.fields.TextField')()),
            ('date_created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('date_submission_closed', self.gf('django.db.models.fields.DateTimeField')(blank=True)),
            ('date_voting_closed', self.gf('django.db.models.fields.DateTimeField')(blank=True)),
            ('admin', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['contest.User'])),
        ))
        db.send_create_signal('contest', ['Contest'])

        # Adding model 'Submission'
        db.create_table('contest_submission', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('sc_url', self.gf('django.db.models.fields.URLField')(max_length=200)),
            ('author', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['contest.User'])),
            ('date_created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal('contest', ['Submission'])

        # Adding model 'Vote'
        db.create_table('contest_vote', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('submission', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['contest.Submission'])),
            ('voter', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['contest.User'])),
            ('score', self.gf('django.db.models.fields.IntegerField')()),
            ('date_created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal('contest', ['Vote'])


    def backwards(self, orm):
        # Deleting model 'User'
        db.delete_table('contest_user')

        # Deleting model 'Contest'
        db.delete_table('contest_contest')

        # Deleting model 'Submission'
        db.delete_table('contest_submission')

        # Deleting model 'Vote'
        db.delete_table('contest_vote')


    models = {
        'contest.contest': {
            'Meta': {'object_name': 'Contest'},
            'admin': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contest.User']"}),
            'date_created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'date_submission_closed': ('django.db.models.fields.DateTimeField', [], {'blank': 'True'}),
            'date_voting_closed': ('django.db.models.fields.DateTimeField', [], {'blank': 'True'}),
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