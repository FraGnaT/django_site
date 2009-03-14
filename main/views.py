# -*- coding: UTF-8 -*-

from django.http import *
from django.shortcuts import render_to_response
from django.contrib import auth
from django.template import Context
from tst.main.models import content, site_setting, Category, Comment_form, Comment


setting = site_setting.objects.get(id=1)  # Временный файл настроек сайта Title, Description, etc.
base = Context({'site':setting, 'Category':Category.objects.all()}) # Основной Context на передачу в шаблон

def post_redirect(request):
    return request.POST.get('redirect', request.META.get('HTTP_REFERER', '/'))

def authrequest(request, commentform=False):               # Добавление в Context по аутентификации
    if request.user.is_authenticated():
        base.update({'user': request.user})
        if commentform:
            base.update({'Comment_form': Comment_form()})
    else:
        from tst.main.models import AuthForm
        base.update({'login_form':AuthForm(request.session)})

def main(request):                        # Заглавная страница
    content_list = content.objects.filter(published = True).order_by('-date')
    base.update({'content':content_list[0:9], 'rss': True, 'category_url': 'latest'})
    authrequest(request)
    return render_to_response('base_preview.html', base)
        

def view_content(request, ID):
    article = content.objects.filter(id=int(ID))
    if not article:
        raise Http404
    base.update({'content':article[0]})
    authrequest(request, True)
    return render_to_response('base_content.html', base)

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
    base.update({'content': content_list, 'rss':True, 'category_url': category})
    authrequest(request)
    return render_to_response('base_preview.html', base)

def category_content(request, category, name):
    content_list = content.objects.filter(category__url=category, title=name, published = True)
    if not content_list:
        raise Http404
    base.update({'content': content_list[0]})
    authrequest(request, True)
    return render_to_response('base_content.html', base)

def test(request, offset):
    return render_to_response('base_preview', {'debug': offset})

def search_all(request):
    if not request.GET:             #Обычный заход на страницу = 404
        raise Http404
    else:
        if request.GET['s'] == '':  #Пустой запрос = 404
            raise Http404
        search_list = content.objects.filter(published = True, text__contains = request.GET['s'])
        if not search_list:
            raise Http404
        base.update({'content': search_list})
        authrequest(request)
        return render_to_response('base_preview.html', base)

def login(request):
    if request.method == 'POST' and not request.user.is_authenticated():
        from tst.main.models import AuthForm
        form = AuthForm(request.session, request.POST)
        if form.is_valid():
            if form.data['openid_url'].count('') > 1:
                after_auth_redirect = form.auth_redirect(post_redirect(request), request.META['HTTP_HOST'])
                print after_auth_redirect
                return HttpResponseRedirect(after_auth_redirect)
            else:
                from django.contrib.auth import authenticate, login
                user = authenticate(username = form.data['username'], password = form.data['password'])
                if not user:
                    return HttpResponseForbidden('Ошибка авторизации')
                if user is not None:
                    login(request, user)
                return HttpResponseRedirect(request.META['HTTP_REFERER'])
        else:
            base.update({'message': form})
            render_to_response('base_simple.html', base)

def logout(request):
    from django.contrib.auth import logout
    logout(request)
    request.session.flush()
    return HttpResponseRedirect(request.META['HTTP_REFERER'])

def auth_openid(request):
    from django.contrib.auth import authenticate, login
    user = authenticate(session=request.session, query=request.GET, return_path=request.path)
    if not user:
        return HttpResponseForbidden('Ошибка авторизации')
    login(request, user)
    return HttpResponseRedirect(request.GET.get('redirect', '/'))

def profile(request, username):
    from django.contrib.auth.models import User
    authrequest(request)
    UserRequest = User.objects.get(username=username)
    CommentCount = Comment.objects.filter(user=UserRequest).count()
    base.update({'UserRequest': UserRequest, 'CommentCount': CommentCount})
    return render_to_response('base_profile.html', base)
