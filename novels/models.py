# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Category(models.Model):
    id = models.CharField(primary_key=True, max_length=255)
    type_name = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'category'


class Charpter(models.Model):
    charpter_id = models.CharField(primary_key=True, max_length=255)
    charpter_name = models.CharField(max_length=255)
    novel = models.ForeignKey('NovelInfo', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'charpter'


class CharpterDetail(models.Model):
    charpter_id = models.CharField(primary_key=True, max_length=255)
    charpter_content = models.TextField()
    charpter_name = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'charpter_detail'


class NovelInfo(models.Model):
    novel_name = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    read_num = models.IntegerField()
    novel_type = models.ForeignKey(Category, models.DO_NOTHING, db_column='novel_type')
    status = models.CharField(max_length=255)
    id = models.CharField(primary_key=True, max_length=255)

    class Meta:
        managed = False
        db_table = 'novel_info'
