from django.shortcuts import render
from django.views import generic


def about(request):
    return render(request, 'pages/about.html')


def rules(request):
    return render(request, 'pages/rules.html')


def page_not_found(request, exception):
    return render(request, 'pages/404.html', status=404)


def csrf_failure(request, reason=''):
    return render(request, 'pages/403csrf.html', status=403)


def server_error(request):
    return render(request, 'pages/500.html', status=500)


class About(generic.TemplateView):
    template_name = 'pages/about.html'


class Rules(generic.TemplateView):
    template_name = 'pages/rules.html'
