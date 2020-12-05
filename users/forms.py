from allauth.account.forms import SignupForm, LoginForm, ResetPasswordForm

class MyCustomLoginForm(LoginForm):

    def __init__(self, *args, **kwargs):
        super(MyCustomLoginForm, self).__init__(*args, **kwargs)
        self.fields['login'].widget.attrs.update({
            'class': 'form-control form-control-lg'
        })
        self.fields['password'].widget.attrs.update({
            'class': 'form-control form-control-lg'
        })
        self.fields['remember'].widget.attrs.update({
            'class': 'mb-3'
        })

class MyCustomSignupForm(SignupForm):

    def __init__(self, *args, **kwargs):
        super(MyCustomSignupForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({
            'class': 'form-control form-control-lg'
        })
        self.fields['email'].widget.attrs.update({
            'class': 'form-control form-control-lg'
        })
        self.fields['password1'].widget.attrs.update({
            'class': 'form-control form-control-lg'
        })
        self.fields['password2'].widget.attrs.update({
            'class': 'form-control form-control-lg'
        })

class MyCustomResetPasswordForm(ResetPasswordForm):

    def __init__(self, *args, **kwargs):
        super(MyCustomResetPasswordForm, self).__init__(*args, **kwargs)
        self.fields['email'].widget.attrs.update({
            'class': 'form-control form-control-lg'
        })
        