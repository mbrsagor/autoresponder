from django.urls import reverse
from django.views import generic
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.contrib.messages.views import SuccessMessageMixin

from user.models import Customer
from user.forms.customer_form import CustomerModelForm


@method_decorator(login_required(login_url='/signin/'), name='dispatch')
class CustomerCreateView(SuccessMessageMixin, generic.CreateView):
    """
    Name: Customer create view
    URL: /create-customer/
    Method: POST
    """
    model = Customer
    form_class = CustomerModelForm
    success_message = 'Customer has been created.'
    success_url = '/user/create-customer/'
    template_name = 'customer/add_customer.html'

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.store = self.request.user.storeOwner
        return super(CustomerCreateView, self).form_valid(form)


@method_decorator(login_required(login_url='/signin/'), name='dispatch')
class CustomerListView(generic.ListView):
    """
    Name: Customer list view
    URL: /customers/
    Method: GET
    """
    model = Customer
    paginate_by = 8
    context_object_name = 'customers'
    template_name = 'customer/customers.html'


@method_decorator(login_required(login_url='/signin/'), name='dispatch')
class CustomerUpdateView(SuccessMessageMixin, generic.UpdateView):
    """
    Name: Customer create view
    URL: /create-customer/
    Method: POST
    :param: pk
    """
    model = Customer
    form_class = CustomerModelForm
    success_message = 'Customer has been updated.'
    success_url = '/user/create-customer/'
    template_name = 'customer/add_customer.html'

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.store = self.request.user.storeOwner
        return super(CustomerUpdateView, self).form_valid(form)

    def get_success_url(self):
        return reverse('update_customer', kwargs={'pk': self.object.id})


@method_decorator(login_required(login_url='/signin/'), name='dispatch')
class CustomerDeleteView(SuccessMessageMixin, generic.DeleteView):
    """
    Name: customer delete view
    URL: /user/customer-delete/<pk>/
    :param
    id
    """
    model = Customer
    success_url = '/user/customers/'
    success_message = 'Customer has been deleted.'
    template_name = 'common/delete_confirm.html'
