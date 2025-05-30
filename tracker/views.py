from django.shortcuts import render
from django.views.generic import ListView
from tracker.models import Operation, Category
from django.http import HttpResponse
from django.views.generic import CreateView, DeleteView, UpdateView, TemplateView
from slugify import slugify
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from .mixins import TrackerMixin, CategoriesMixin
from django.contrib.auth.decorators import login_required


class TrackerHome(TrackerMixin, TemplateView):
    template_name = 'base.html'


class CreateOperation(LoginRequiredMixin, TrackerMixin, CategoriesMixin, CreateView):
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


    # def get_form(self, form_class=None):
    #     form = super().get_form(form_class)
    #     user = self.request.user
    #     form.fields['category'].queryset = Category.objects.filter(user=user)
    #
    #     return form


class CreateCategory(LoginRequiredMixin, TrackerMixin, CreateView):
    model = Category
    fields = ['name']
    template_name = 'tracker/create.html'
    extra_context = {'title': 'Создание категории'}

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context['categories'] = Category.objects.all()
    #     return context

    def form_valid(self, form):
        obj = form.save(commit=False)
        base_slug = slugify(obj.name)
        count = Category.objects.filter(slug__startswith=base_slug).count()
        obj.slug = f"{base_slug}{count + 1}" if count else base_slug
        obj.user_id = self.request.user.id
        return super().form_valid(form)


class DeleteCategory(LoginRequiredMixin, TrackerMixin, DeleteView):
    model = Category
    template_name = 'tracker/delete.html'
    success_url = reverse_lazy('home')
    extra_context = {'title': 'Удаление категории'}

    def get_queryset(self):
        return Category.objects.filter(user=self.request.user)

    def delete(self, request, *args, **kwargs):
        response = super().delete(request, *args, **kwargs)
        return response


class DeleteOperation(LoginRequiredMixin, DeleteView):
    model = Operation
    template_name = 'tracker/delete.html'
    success_url = reverse_lazy('home')
    extra_context = {'title': 'Удаление операции'}

    def get_queryset(self):
        return Operation.objects.filter(user=self.request.user)



    def delete(self, request, *args, **kwargs):
        response = super().delete(request, *args, **kwargs)
        return response


class UpdateCategory(LoginRequiredMixin, TrackerMixin,  UpdateView):
    model = Category
    fields = ['name']
    template_name = 'tracker/update.html'
    success_url = reverse_lazy('home')

    def get_queryset(self):
        return Category.objects.filter(user=self.request.user)

    def form_valid(self, form):
        obj = form.save(commit=False)
        base_slug = slugify(obj.name)
        count = Category.objects.filter(slug__startswith=base_slug).count()
        obj.slug = f"{base_slug}{count + 1}" if count else base_slug
        return super().form_valid(form)


class UpdateOperation(LoginRequiredMixin, TrackerMixin, CategoriesMixin,  UpdateView):
    model = Operation
    fields = ['name', 'amount', 'method', 'type', 'category']
    template_name = 'tracker/update.html'
    success_url = reverse_lazy('home')

    def get_queryset(self):
        return Operation.objects.filter(user=self.request.user)

    def form_valid(self, form):
        obj = form.save(commit=False)
        base_slug = slugify(obj.name)
        count = Operation.objects.filter(slug__startswith=base_slug).count()
        obj.slug = f"{base_slug}{count + 1}" if count else base_slug
        return super().form_valid(form)


class AllOperations(LoginRequiredMixin, TrackerMixin, ListView):
    template_name = 'tracker/index.html'
    context_object_name = 'operations'

    def get_queryset(self):
        return Operation.objects.filter(user_id=self.request.user.id)
        # return Operation.objects.all().values('name', 'amount', 'type', 'category')





class Incomes(LoginRequiredMixin, TrackerMixin, ListView):
    template_name = 'tracker/index.html'
    context_object_name = 'operations'
    extra_context = {'view': 'incomes'}
    def get_queryset(self):
        return Operation.objects.filter(type=1, user_id=self.request.user.id) # 1 = доход

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context['view'] = 'incomes'
    #     context['categories'] = Category.objects.all()
    #     return context


class Expenses(LoginRequiredMixin, TrackerMixin, ListView):
    template_name = 'tracker/index.html'
    context_object_name = 'operations'
    extra_context = {'view': 'expenses'}

    def get_queryset(self):
        return Operation.objects.filter(type=0, user_id=self.request.user.id) # 1 = доход




@login_required
def visual_report(request):
    op_type = request.GET.get('type', 'expense')
    chart_type = request.GET.get('chart', 'bar')

    if op_type == 'income':
        type_value = Operation.TransactionType.INCOME
        op_type_label = "Доходы"
    else:
        type_value = Operation.TransactionType.EXPENSE
        op_type_label = "Расходы"

    operations = Operation.objects.filter(user=request.user, type=type_value)

    data = {}
    for op in operations:
        cat_name = op.category.name if op.category else "Без категории"
        data[cat_name] = data.get(cat_name, 0) + op.amount

    labels = list(data.keys())
    values = list(data.values())

    return render(request, 'tracker/visual_report.html', {
        'labels': labels,
        'values': values,
        'title': "Отчет по операциям",
        'op_type_label': op_type_label,
        'chart_type': chart_type
    })


