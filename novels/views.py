from django.shortcuts import render_to_response,get_object_or_404
from .models import NovelInfo,Category,Charpter,CharpterDetail
from django.core.paginator import Paginator
# Create your views here.




#base.html
def base(request):
	novel_types = Category.objects.all()
	context = {}
	context['novel_types'] = novel_types
	return render_to_response('base.html',context)




#小说的章节目录
def charpter_contents(request,novel_pk):
	charpter_contents = Charpter.objects.filter(novel_id = novel_pk) #filter不同外键
	novel = get_object_or_404(NovelInfo, pk= novel_pk)
	novel_types = Category.objects.all()  

	context = {}
	context['novel'] = novel              #提供小说信息
	context['novel_types'] = novel_types  #给上一个附和页面提供数据
	context['charpter_contents'] = charpter_contents
	return render_to_response('charpter_contents.html',context)


#章节具体内容
def charpter_detail(request,charpter_pk):
	charpter_detail = CharpterDetail.objects.get(charpter_id=charpter_pk)
	novel_types = Category.objects.all()

	context = {}
	context['charpter_detail'] = charpter_detail
	context['novel_types'] = novel_types  #给上一个附和页面提供数据
	return render_to_response('charpter_detail.html',context)


#搜索小说功能
def search(request):
	q= request.GET.get('q')
	novel_types = Category.objects.all()
	context = {}

	if q:
		results = NovelInfo.objects.filter(novel_name__icontains = q)
		context['results'] = results
		context['novel_types'] = novel_types  #给上一个附和页面提供数据
		return render_to_response('search.html',context)


#分页功能
def paginator(novels,request):
	page_num = request.GET.get('page',1)
	paginator = Paginator(novels,25)  #25部小说分一页
	page_of_novels = paginator.get_page(page_num)
	page_sum = paginator.num_pages        #总页数
	current_page = page_of_novels.number  # 获取当前页码

	context = {}
	context['page_of_novels'] = page_of_novels
	context['page_sum'] =page_sum     #总页数
	context['current_page'] = current_page
	return context


#首页
def index(request):
	novels_info = NovelInfo.objects.all()[:100]
	novel_types = Category.objects.all()
	context = paginator(novels_info,request)
	
	context['novel_types'] = novel_types
	return render_to_response('index.html',context)


#不同类型的小说
def novel_type(request,category_pk):
	category = get_object_or_404(Category, pk=category_pk)
	novels_with_type = NovelInfo.objects.filter(novel_type = category)
	context = paginator(novels_with_type,request)  #25部小说分一页
	
	novel_types = Category.objects.all()  
	context['novel_type'] = category      #用来写页面的title
	context['novel_types'] = novel_types  #给上一个附合页面提供数据
	return render_to_response('novels_with_type.html',context)

