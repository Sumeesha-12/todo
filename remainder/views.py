from django.shortcuts import render,redirect
from django.views.generic import View
from remainder.forms import UserForm,LoginForm,TodoForm
from django.contrib.auth import authenticate,login,logout
from remainder.models import Todos
from django.utils.decorators import method_decorator


def sigin_required(fn):
    def wrapper(request,*args,**kwargs):
        if not request.user.is_authenticated:
            return redirect("signin")
        else:
            return fn(request,*args,**kwargs)
    return wrapper
def owner_permission_required(fn):
    def wrapper(request,*args,**kwargs):
        id=kwargs.get("pk")
        todo_object=Todos.objects.get(id=id)
        if todo_object.user != request.user:
            return redirect("signin")
        else:
            return fn(request,*args,**kwargs)
    return wrapper



# Create your views here.
class SignUpView(View):

    def get (self,request,*args,**kwargs):
        form=UserForm()
        return render (request,"register.html",{"form":form})
    def post(self,request,*args,**kwargs):
        form=UserForm(request.POST)
        if form.is_valid():
            form.save()
            print("Account Created")
            return redirect("register")
        else:
            print("failed")
            return render (request,"register.html",{"form":form})
        
class SignInView(View):
    def get (self,request,*args,**kwargs):
        form=LoginForm()
        return render(request,"login.html",{"form":form})
    def post(self,request,*args,**kwargs):
        form=LoginForm(request.POST)
        if form.is_valid():
            uname=form.cleaned_data.get("username")
            pwd=form.cleaned_data.get("password")
            user_object=authenticate(request,username=uname,password=pwd)
            if user_object:
                login(request,user_object)
                print("Sucessfully Login")
                return redirect("index")
        print("invalid credential")
        return render(request,"login.html",{"form":form})
    
decs=[sigin_required,owner_permission_required]

@method_decorator(sigin_required,name="dispatch")   
class IndexView(View):
    def get(self,request,*args,**kwargs):
        form=TodoForm()
        qs=Todos.objects.filter(user=request.user).order_by("status")
        return render(request,"index.html",{"form":form,"data":qs})
    def post(self,request,*args,**kwargs):
        form=TodoForm(request.POST)
        if form.is_valid():
            form.instance.user=request.user
            form.save()
            return redirect("index")
        else:
            return render(request,"index.html",{"form":form})
        
# localhost:8000/todos/{id}/remove/
@method_decorator(decs,name="dispatch")
class TodoDeleteView(View):
    def get(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        Todos.objects.filter(id=id).delete()
        return redirect("index")

# localhost:8000/todos/{id}/change/
@method_decorator(decs,name="dispatch")
class TodoEditView(View):
    def get(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        todo_object=Todos.objects.get(id=id)
        if todo_object.status==True:
            todo_object.status=False
            todo_object.save()
        else:
            todo_object.status=True
            todo_object.save()
        # Todos.objects.filter(id=id).update(status=True)
        return redirect("index")
    
@method_decorator(sigin_required,name="dispatch")   
class SignOutView(View):
    def get(self,request,*args,**kwargs):
        logout(request)
        return redirect("signin")
    
        



            
            

    









    

