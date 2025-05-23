from django.shortcuts import render
from django.views.generic import ListView
from tracker.models import Operation, Category
from django.http import HttpResponse
from django.views.generic import CreateView, DeleteView, UpdateView, TemplateView
from slugify import slugify
from django.urls import reverse_lazy


class TrackerHome(TemplateView):
    template_name = 'base.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        return context


class CreateOperation(CreateView):
    model = Operation
    fields = ['name', 'amount', 'method', 'type', 'category']
    title_page = 'Добавление операции'
    template_name = 'tracker/create.html'
    extra_context = {'title': 'Создание Операции'}

    def form_valid(self, form):
        obj = form.save(commit=False)
        base_slug = slugify(obj.name)
        count = Operation.objects.filter(slug__startswith=base_slug).count()
        obj.slug = f"{base_slug}{count + 1}" if count else base_slug
        obj.user = self.request.user
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        return context


class CreateCategory(CreateView):
    model = Category
    fields = ['name']
    template_name = 'tracker/create.html'
    extra_context = {'title': 'Создание категории'}

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        return context

    def form_valid(self, form):
        obj = form.save(commit=False)
        base_slug = slugify(obj.name)
        count = Category.objects.filter(slug__startswith=base_slug).count()
        obj.slug = f"{base_slug}{count + 1}" if count else base_slug
        obj.user_id = self.request.user.id
        return super().form_valid(form)


class DeleteCategory(DeleteView):
    model = Category
    template_name = 'tracker/delete.html'
    success_url = reverse_lazy('home')
    extra_context = {'title': 'Удаление категории'}

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def delete(self, request, *args, **kwargs):
        response = super().delete(request, *args, **kwargs)
        return response


class DeleteOperation(DeleteView):
    model = Operation
    template_name = 'tracker/delete.html'
    success_url = reverse_lazy('home')
    extra_context = {'title': 'Удаление операции'}

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def delete(self, request, *args, **kwargs):
        response = super().delete(request, *args, **kwargs)
        return response


class UpdateCategory(UpdateView):
    model = Category
    fields = ['name']
    template_name = 'tracker/update.html'
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        obj = form.save(commit=False)
        base_slug = slugify(obj.name)
        count = Category.objects.filter(slug__startswith=base_slug).count()
        obj.slug = f"{base_slug}{count + 1}" if count else base_slug
        return super().form_valid(form)


class UpdateOperation(UpdateView):
    model = Operation
    fields = ['name', 'amount', 'method', 'type', 'category']
    template_name = 'tracker/update.html'
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        obj = form.save(commit=False)
        base_slug = slugify(obj.name)
        count = Operation.objects.filter(slug__startswith=base_slug).count()
        obj.slug = f"{base_slug}{count + 1}" if count else base_slug
        return super().form_valid(form)


class AllOperations(ListView):
    template_name = 'tracker/index.html'
    context_object_name = 'operations'

    def get_queryset(self):
        return Operation.objects.all()
        # return Operation.objects.all().values('name', 'amount', 'type', 'category')


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['view'] = 'all'
        context['categories'] = Category.objects.all()
        return context


class Incomes(ListView):
    template_name = 'tracker/index.html'
    context_object_name = 'operations'

    def get_queryset(self):
        return Operation.objects.filter(type=1) # 1 = доход

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['view'] = 'incomes'
        context['categories'] = Category.objects.all()
        return context


class Expenses(ListView):
    template_name = 'tracker/index.html'
    context_object_name = 'operations'

    def get_queryset(self):
        return Operation.objects.filter(type=0) # 1 = доход

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['view'] = 'expenses'
        context['categories'] = Category.objects.all()
        return context



def visual_report(request):
    return HttpResponse("Визуальный отчет")

def feedback(request):
    return HttpResponse("Фидбэк")

