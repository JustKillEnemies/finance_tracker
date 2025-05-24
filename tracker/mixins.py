from .models import Category

class TrackerMixin:
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            context['categories'] = Category.objects.filter(user_id=self.request.user.id)
        else:
            context['categories'] = []
        return context




class CategoriesMixin:
    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        user = self.request.user
        form.fields['category'].queryset = Category.objects.filter(user=user)

        return form
