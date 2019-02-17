# NovelWeb-python-Django

### 一.首先来看看目标网站
      （图片1）小说信息
      （图片2）小说目录
      （图片3）小说详情页
      这个网站所需要爬取的数据都是用js技术动态渲染的页面，所以可以选择selenium来模拟浏览器来爬取数据。

### 二.用到的技术：
   框架：Django<br> 数据库：MYSQL<br> 自定义爬虫：装饰器，多线程，selenium库<br>
   
### 二.内在逻辑
   一般来说，小说的页面有三种，小说的大体信息，小说章节，小说具体内容，还有小说的分类。对应于Django的model层，有四种。
   
 ···python
 class Category(models.Model):
    id = models.CharField(primary_key=True, max_length=255)
    type_name = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'category'

···
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
  '''
