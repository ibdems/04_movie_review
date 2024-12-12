from allauth.account.views import SignupView

from myauth.forms import CustomSignupForm

# Create your views here.


class CustomSignupView(SignupView):
    form_class = CustomSignupForm

    def get_form_class(self):
        return self.form_class
