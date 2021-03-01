from django.shortcuts import render, redirect
from operator import attrgetter
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from app_settings.models import SideMenu
from account.models import Visit
from django.http import HttpResponse
from django.http import HttpResponseRedirect
BLOG_POSTS_PER_PAGE = 10

def home_screen_view(request, *args, **kwargs):
	return HttpResponseRedirect('/login')
	
# 	context = {}

# 	# Search
# 	query = ""
# 	if request.GET:
# 		query = request.GET.get('q', '')
# 		context['query'] = str(query)

# 	blog_posts = sorted(get_blog_queryset(query), key=attrgetter('date_updated'), reverse=True)
	


# 	# Pagination
# 	page = request.GET.get('page', 1)
# 	blog_posts_paginator = Paginator(blog_posts, BLOG_POSTS_PER_PAGE)
# 	try:
# 		blog_posts = blog_posts_paginator.page(page)
# 	except PageNotAnInteger:
# 		blog_posts = blog_posts_paginator.page(BLOG_POSTS_PER_PAGE)
# 	except EmptyPage:
# 		blog_posts = blog_posts_paginator.page(blog_posts_paginator.num_pages)

# 	context['blog_posts'] = blog_posts

# 	return render(request, "personal/home.html", context)


def  dashboard_view(request):
	# return HttpResponse('dashboard_view')
	menus = SideMenu.objects.filter(parent_id=None).order_by('order').all()
	visits = Visit.objects.order_by('-id').all()
	ctx = {'menus' : menus,'visits': visits}
	return render(request, 'personal/dashboard_layout/dashboard.html', ctx)


