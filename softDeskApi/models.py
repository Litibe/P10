from django.conf import settings
from django.db import models
from django.utils import timezone


class Project(models.Model):
    class Type_project(models.TextChoices):
        BACK_END = 'BACK_END'
        FRONT_END = 'FRONT_END'
        IOS = 'IOS'
        ANDROID = 'ANDROID'

    title = models.CharField(max_length=128, verbose_name="Project Title")
    description = models.TextField(max_length=2048, verbose_name="Description")
    type = models.CharField(choices=Type_project.choices, max_length=15)
    author_user = models.ForeignKey(
        to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE)


class Contributor(models.Model):
    class Permission_contributor(models.TextChoices):
        AUTHOR = 'AUTHOR'
        CONTRIBUTOR = 'CONTRIBUTOR'

    user = models.ForeignKey(
        to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    role = models.CharField(
        choices=Permission_contributor.choices, max_length=20, verbose_name="Contributor Role")


class Issue(models.Model):
    class Tag_issue(models.TextChoices):
        BUG = 'BUG'
        IMPROVEMENT = 'IMPVMT'
        TASK = 'TASK'

    class Priority_issue(models.TextChoices):
        HIGH = 'HIGH'
        MEDIUM = 'MEDIUM'
        LOW = 'LOW'

    class Status_issue(models.TextChoices):
        TO_DO = 'TO_DO'
        IN_PROGRESS = 'IN_PROGRESS'
        TERMINATED = 'TERMINATED'
    title = models.CharField(max_length=128, verbose_name="Project Title")
    description = models.TextField(max_length=2048, verbose_name="Description")
    tag = models.CharField(choices=Tag_issue.choices, max_length=15)
    priority = models.CharField(
        choices=Priority_issue.choices, max_length=15)
    projet = models.ForeignKey(
        Project, on_delete=models.CASCADE, verbose_name="Project Id", related_name="Project")
    status = models.CharField(
        choices=Status_issue.choices, max_length=15)
    author_user = models.ForeignKey(
        to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name="Author User Id", related_name="Author_User_Id")
    assignee_user = models.ForeignKey(
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
