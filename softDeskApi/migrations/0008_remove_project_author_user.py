# Generated by Django 4.0 on 2021-12-28 17:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('softDeskApi', '0007_alter_contributor_role_alter_issue_priority_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='project',
            name='author_user',
        ),
    ]