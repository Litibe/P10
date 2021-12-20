from django.conf import settings
from django.db import models
from django.utils import timezone


class Project(models.Model):
    title = models.CharField(max_length=128, verbose_name="Project Title")
    description = models.TextField(max_length=2048, verbose_name="Description")

    class Type_project(models.TextChoices):
        BACK_END = 'BE'
        FRONT_END = 'FE'
        IOS = 'IOS'
        ANDROID = 'AID'
    type = models.fields.CharField(choices=Type_project.choices, max_length=5)
    author_user_id = models.ForeignKey(
        to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE)


class Contributor(models.Model):
    user_id = models.ForeignKey(
        to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    project_id = models.ForeignKey(Project, on_delete=models.CASCADE)

    class Permission_contributor(models.TextChoices):
        AUTHOR = 'AUTH'
        CONTRIBUTOR = 'CONTRI'
    type = models.fields.CharField(
        choices=Permission_contributor.choices, max_length=20)
    role = models.CharField(max_length=128, verbose_name="Contributor Role")


class Issue(models.Model):
    title = models.CharField(max_length=128, verbose_name="Project Title")
    description = models.TextField(max_length=2048, verbose_name="Description")

    class Tag_issue(models.TextChoices):
        BUG = 'BUG'
        IMPROVEMENT = 'IMPVMT'
        TASK = 'TASK'
    tag = models.fields.CharField(choices=Tag_issue.choices, max_length=15)

    class Priority_issue(models.TextChoices):
        HIGH = 'P2'
        MEDIUM = 'P1'
        LOW = 'P0'
    priority = models.fields.CharField(
        choices=Priority_issue.choices, max_length=6)

    class Status_issue(models.TextChoices):
        TO_DO = 'S2'
        IN_PROGRESS = 'S1'
        TERMINATED = 'S0'
    status = models.fields.CharField(
        choices=Status_issue.choices, max_length=6)
    author_user_id = models.ForeignKey(
        to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name="Author User Id", related_name="Author_User_Id")
    assignee_user_id = models.ForeignKey(
        to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name="Assignee User Id", related_name="Assignee_User_Id")
    created_time = models.DateTimeField(
        default=timezone.now)


class Comment(models.Model):
    description = models.TextField(max_length=2048, verbose_name="Description")
    author_user_id = models.ForeignKey(
        to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name="Author User Id")
    issue_id = models.ForeignKey(
        Issue, on_delete=models.CASCADE, verbose_name="Issue Id")
    created_time = models.DateTimeField(
        default=timezone.now)
