from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from .forms import UserSignup
from django.contrib.auth import login,logout,authenticate
from django.contrib import messages
from django.contrib.auth.views import PasswordResetConfirmView


#to make custom Password reset
class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    def form_valid(self, form):
        form.save()
        messages.success(self.request, "Your password has been reset successfully! Please log in with your new password.")
        return redirect('signin')

# Create your views here.
def usersignup(request):
    if request.method == 'POST':
        fm= UserSignup(request.POST)
        if fm.is_valid():
            user=fm.save()
            login(request,user)
            return redirect('home')
        else:
            for error in fm.errors.values():
                messages.error(request, error)
    return render(request,'auths/signup.html')

    # if request.method == 'POST':
    #     name = request.POST.get('username')
    #     email = request.POST.get('email')
    #     password = request.POST.get('password1')
    #     user = User.objects.create(username=name,email=email)
    #     user.set_password(password)
    #     user = User.save()
    #     login(request,user)
    #     return redirect('home')
    # return render(request,'auths/signup.html')
    

def usersignin(request):
    if request.method == 'POST':
        email = request.POST['email']
        passwords=request.POST['password']
        # usered = User.objects.filter(email=email)           #getting multiple values  /// querysets
        try:
            usered = User.objects.get(email=email)
        except:
            messages.error(request,'Credentials not matched')
            # print('exception run')
            return redirect('signin')
        # username=user.username
        username = usered.username
        user = authenticate(request,username=username,password=passwords)

        if user is not None:
            login(request,user)
            return redirect('home')
        else:
            print('nhi')
    return render(request,'auths/signin.html')

def userlogout(request):
    logout(request)
    return redirect('home')