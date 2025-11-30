from django.views import View
from django.contrib import messages
from django.shortcuts import redirect
from django.contrib.auth import login, logout
from django.contrib.auth.views import LoginView
from django.shortcuts import resolve_url, render
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.decorators import login_required

from user.forms.auth_form import LoginForm


class SignInView(LoginView):
    """
    Name: Merchant SignIn view
    URL: signin/
    :param
    email
    phone_number
    """
    authentication_form = LoginForm
    form_class = LoginForm
    redirect_authenticated_user = False
    template_name = 'auth/signin.html'

    def get_success_url(self):
        url = self.get_redirect_url()
        return url or resolve_url('/dashboard/')

    def form_valid(self, form):
        remember_me = form.cleaned_data['remember_me']
        login(self.request, form.get_user())

        if remember_me:
            self.request.session.set_expiry(1209600)
        return super(SignInView, self).form_valid(form)


class SignOutView(View):
    """
    Name: Logout view
    URL: signout/
    """

    def get(self, request):
        logout(request)
        return redirect('/user/signin/')


@login_required
def change_password(request):
    """
    Password Change
    :param request:
    :return:
    URL: user/password_change/
    """
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Your password was successfully updated!')
            return redirect('password_change')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'auth/change_password.html', {
        'form': form
    })
