from django.shortcuts import render
from django.views.generic import ListView
from tracker.models import Operation
from django.http import HttpResponse

class TrackerHome(ListView):
    # model = Operation
    template_name = 'tracker/index.html'
    context_object_name = 'operations'

    def get_queryset(self):
        return Operation.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # тут закинем переменную в контекст
        context['title'] = "Главная страница"
        return context


def operations(request):
    return HttpResponse("Все операции")

def incomes(request):
    return HttpResponse("Все доходы")

def expenses(request):
    return HttpResponse("Все расходы")

def visual_report(request):
    return HttpResponse("Визуальный отчет")