# -*- coding: UTF-8 -*-

from django.http import *
from django.shortcuts import render_to_response
from django.contrib import auth
from django.template import Context
from tst.main.models import content, site_setting, Category, Login_form, Comment_form, Comment


setting = site_setting.objects.get(id=1)  # Временный файл настроек сайта Title, Description, etc.
def post_redirect(request):
    return request.POST.get('redirect', request.META.get('HTTP_REFERER', '/'))

def main(request):
    content_list = content.objects.filter(published = True).order_by('-date')
    return render_to_response('base_preview.html', {'content': content_list[0:9], 'rss': True, 'site':setting, 'Category':\
            Category.objects.all(), 'login_form': Login_form(), 'user': request.user, 'category_url': 'latest'})
        

def view_content(request, ID):
    article = content.objects.filter(id=int(ID))
    if not article:
        raise Http404
    return render_to_response('base_content.html', {'content': article[0], 'site':setting, 'rss':True, 'Category':\
        Category.objects.all(), 'user': request.user, 'login_form': Login_form(), 'Comment_form': Comment_form()})

def add(request, offset):                                        #Добавление комментария
    ctnt = content.objects.get(id=int(offset))
    if not ctnt:
        raise Http404
    if request.user.is_authenticated():
        if request.method == 'POST':
            form = Comment_form(request.POST)
            if form.is_valid():
                text = form.cleaned_data['text']
                new = Comment(user=request.user, text=text)
                new.save()
                ctnt.comment.add(Comment.objects.get(id=new.id))
                return HttpResponseRedirect("/id"+offset)

def del_comment(request, ID):
    if request.user.is_superuser:
        commentdel = Comment.objects.get(id=int(ID))
        contentdel = content.objects.get(comment=commentdel)
        contentdel.comment.remove(commentdel)
        commentdel.delete()
        return render_to_response('base_simple.html', {'message':'Комментарий ID: %s с текстом %s успешно удалён.'})
    else:
        raise Http404

def category_views(request, category):                             #Вывод категории
    content_list = content.objects.filter(category__url = category, published = True)
    if not content_list:
        raise Http404
    return render_to_response('base_preview.html', {'content': content_list, 'site':setting, 'rss':True, 'Category':\
            Category.objects.all(), 'login_form': Login_form(), 'user': request.user, 'category_url': category})

def category_content(request, category, name):
    content_list = content.objects.filter(category__url=category, title=name, published = True)
    if not content_list:
        raise Http404
    return render_to_response('base_content.html', {'content': content_list[0], 'site':setting, 'Category':\
        Category.objects.all(), 'user': request.user, 'login_form': Login_form(), 'Comment_form': Comment_form()})

def test(request, offset):
    return render_to_response('base_preview.html', {'debug': offset})

def search_all(request):
    if not request.GET:             #Обычный заход на страницу = 404
        raise Http404
    else:
        if request.GET['s'] == '':  #Пустой запрос = 404
            raise Http404
        search_list = content.objects.filter(published = True, text__contains = request.GET['s'])
        if not search_list:
            raise Http404
        return render_to_response('base_preview.html', {'content': search_list, 'site':setting, 'Category':\
            Category.objects.all(), 'login_form': Login_form(), 'user': request.user})
#OPENID
from openid.consumer.consumer import Consumer
from openid.store.filestore import FileOpenIDStore
from django.conf import settings
def render_to_redirect(request, template_name, context_dict, **kwargs):          #Temp для редиректа
    from django.template import RequestContext
    from django.shortcuts import render_to_response as _render_to_response
    context = RequestContext(request, context_dict)
    return _render_to_response(template_name, context_instance=context, **kwargs)


def get_consumer(session):
    if not settings.OPENID_STORE_ROOT:
        raise Exception('OPENID_STORE_ROOT is not set')
    return Consumer(session, FileOpenIDStore(settings.OPENID_STORE_ROOT))


def auth_openid(request):
    return render_to_response('.sddahtml', {'message':request.GET['openid.claimed_id']})

       
def login_openid(request):
    from tst.main.models import AuthForm
    if request.method == 'POST':
        form = AuthForm(request.session, request.POST)
        if form.is_valid():
            after_auth_redirect = form.auth_redirect(post_redirect(request), 'tst.main.views.auth_openid')
            print after_auth_redirect
            return HttpResponseRedirect(after_auth_redirect)
        redirect = post_redirect(request)
    else:
        form = AuthForm(request.session)
        redirect = request.GET.get('redirect', '/')
    return render_to_redirect(request, 'base_simple.html', {'form': form, 'redirect': redirect})
