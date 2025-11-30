from django.urls import reverse
from django.views import generic
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.contrib.messages.views import SuccessMessageMixin

from user.models import Supplier
from user.forms.supplier_form import SupplierModelForm


@method_decorator(login_required(login_url='/signin/'), name='dispatch')
class SupplierCreateView(SuccessMessageMixin, generic.CreateView):
    """
    Name: Customer create view
    URL: /user/create-customer/
    Method: POST
    """
    model = Supplier
    form_class = SupplierModelForm
    success_message = 'Supplier has been created.'
    success_url = '/user/create-supplier/'
    template_name = 'suppliers/add_suppliers.html'

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.store = self.request.user.storeOwner
        return super(SupplierCreateView, self).form_valid(form)


@method_decorator(login_required(login_url='/signin/'), name='dispatch')
class SupplierListView(generic.ListView):
    """
    Name: Supplier list view
    URL: /user/suppliers/
    Method: GET
    """
    model = Supplier
    paginate_by = 8
    context_object_name = 'suppliers'
    template_name = 'suppliers/suppliers.html'


@method_decorator(login_required(login_url='/signin/'), name='dispatch')
class SupplierUpdateView(SuccessMessageMixin, generic.UpdateView):
    """
    Name: Customer create view
    URL: /user/create-customer/
    Method: POST
    """
    model = Supplier
    form_class = SupplierModelForm
    success_message = 'Supplier has been updated.'
    template_name = 'suppliers/add_suppliers.html'

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.store = self.request.user.storeOwner
        return super(SupplierUpdateView, self).form_valid(form)

    def get_success_url(self):
        return reverse('update_supplier', kwargs={'pk': self.object.id})


@method_decorator(login_required(login_url='/signin/'), name='dispatch')
class SupplierDeleteView(SuccessMessageMixin, generic.DeleteView):
    """
    Name: Supplier delete view
    URL: user/supplier-delete/<pk>/
    :param
    id
    """
    model = Supplier
    success_url = '/user/suppliers/'
    success_message = 'Supplier has been deleted.'
    template_name = 'common/delete_confirm.html'
