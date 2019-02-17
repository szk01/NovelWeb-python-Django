# NovelWeb-python-Django

### 一.首先来看看目标网站
      （图片1）小说信息
      （图片2）小说目录
      （图片3）小说详情页
      这个网站所需要爬取的数据都是用js技术动态渲染的页面，所以可以选择selenium来模拟浏览器来爬取数据。

### 二.用到的技术：
   框架：Django<br> 数据库：MYSQL<br> 自定义爬虫：装饰器，多线程，selenium库<br>
   
### 二.内在逻辑
   一般来说，小说的页面有三种，小说的分类，小说章节，小说具体内容，还有小说的分类。对应于Django的model层，有四种。

小说分类 
```python
 
 class Category(models.Model):
    id = models.CharField(primary_key=True, max_length=255)
    type_name = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'category'

```
小说章节（即目录）
```python
class Charpter(models.Model):
    charpter_id = models.CharField(primary_key=True, max_length=255)
    charpter_name = models.CharField(max_length=255)
    novel = models.ForeignKey('NovelInfo', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'charpter'
```
具体小说内容
```python
class CharpterDetail(models.Model):
    charpter_id = models.CharField(primary_key=True, max_length=255)
    charpter_content = models.TextField()
    charpter_name = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'charpter_detail'
```
小说相关信息（小说名，作者，阅读数...）
```python
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
```

### 爬虫逻辑。目标网站主要有三种页面，那么就写三个爬虫，在实际爬取的过程中，遇到了各种不同的问题，也用到了不同的技术来解决。
    1.爬取小说相关信息,相关代码位于function/spider/spider_novel_info.py.（下面代码只是小部分代码）
      根据目标网站的情况，需要实现翻页功能，根据selenium库的方法，根据情况具体编写的实现功能
     
    ```python
    def get_next_page(num):
    url = 'https://book.tianya.cn/html2/allbooks-cat.aspx?cat_bigid=2&cat_id=25'    #科幻小说6/5
    browser.get(url)
    try:
        print('\n\n翻到第%d页' % num)
        input = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "page")))
        input.clear()
        input.send_keys(num)
        input.send_keys(Keys.ESCAPE)  # 输入回车键
        time.sleep(8)    #等待数据渲染完成
        html = browser.page_source
        return html
    except TimeoutError as e:
        print(e)
```
   2.爬取小说的章节信息，相关代码位于function/spider/spider_charpter_info.py.
     为了提高爬取的速度，可以使用selenium的显示等待方式（以下是部分代码）
     ```python
     def click_href(url):
    try:
        browser.get(url)
        wait = WebDriverWait(browser, 20)
        # 显示等待,小说页面加载完成
        content_click = wait.until(EC.element_to_be_clickable((By.CLASS_NAME,'directory'))).click()
        # browser.find_element_by_link_text('目录').click()
        time.sleep(4)
        contents = wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'contents')))
        html = browser.page_source
        return html
    except:
        html = click_href(url)
        return html
    ```
    3.爬取小说的具体章节，这是数据最多的一部分，也是最难得一部分。
      由于数据太多，在爬取的过程中，由于网络不佳或其他原因使得一个页面总是无法加载出来，在用显示等待的过程中超时而抛出异常，导致整个程序无法运行，因此在有必要时跳过这个爬取，进行下一个页面的爬取。
      解决方法：使用python的装饰器以及多进程来实现规定某函数的运行时间，超时后程序也不会抛出异常。
      ```python
      
#装饰器，给get_one_cahrpter_content(url)函数新增功能
def time_limited_pri(time_limited):
    def wrapper(func):  #接收的参数是函数
        def __wrapper(params):
            class TimeLimited(Thread):  #class中的两个函数是必须的
                def __init__(self):
                    Thread.__init__(self)

                def run(self):
                    func(params)

            t = TimeLimited()
            t.setDaemon(True)  #这个用户线程必须设置在start()前面
            t.start()
            t.join(timeout=time_limited)
            if t.is_alive():
                raise Exception('连接超时')

        return __wrapper

    return wrapper

#获取免费章节的文本内容
@time_limited_pri(15)
def get_one_charpter_content(url):
    try:
        browser.get(url)
        wait = WebDriverWait(browser, 20)
        contents = wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'bd')))
        # time.sleep(2)
        html = browser.page_source
        doc = pq(html)
        content = doc('.bd').html().replace('<br xmlns="http://www.w3.org/1999/xhtml"/>', '\n\n')
        # data['novel_id'] = doc('#main').attr('bookid')
        # print(data['novel_id'])
        return content
    except:
        content = get_one_charpter_content(url)
        return content
```
    





































