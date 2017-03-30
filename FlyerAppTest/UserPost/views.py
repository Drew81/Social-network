from django.views import generic
from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.utils import timezone
from .models import Post, Details, UserProfile
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.core.urlresolvers import reverse_lazy
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from django.views.generic import View
from .forms import UserForm, EditProfileForm, RegistrationForm
from django.contrib.auth.models import User
# Create your views here.


class IndexView(generic.ListView):
    template_name = 'UserPost/index.html'
    context_object_name = 'all_post'

    def get_queryset(self):
        return Post.objects.all()


class DetailView(generic.DetailView):
    model = Post
    template_name = 'UserPost/detail.html'


class PostCreate(CreateView):
    model = Post
    fields = ['image', 'name', 'about', 'address', 'zip', 'city']
    success_url = reverse_lazy('UserPost:detail-add')


class ProfileCreate(CreateView):
    model = UserProfile
    fields = ['bio', 'profile_image']
    success_url = reverse_lazy('UserPost/profile.html')


class DetailsCreate(CreateView):
    model = Details
    fields = ['details']
    success_url = reverse_lazy('UserPost/index.html')


class PostUpdate(UpdateView):
    model = Post
    fields = ['image', 'name', 'about', 'address', 'zip']


class PostDelete(DeleteView):
    model = Post
    success_url = reverse_lazy('UserPost:index')


class UserFormView(View):
    form_class = UserForm
    template_name = 'UserPost/reg_form.html'

    def get(self, request):
        form = self.form_class(None)
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)

        if form.is_valid():

            user = form.save(commit=False)

            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user.set_password(password)
            user.save()

            user = authenticate(username=username, password=password)

            if user is not None:

                if user.is_active:
                    login(request, user)
                    return redirect('UserPost:index')

        return render(request, self.template_name, {'form': form})


class LoginFormView(View):
    form_class = UserForm
    template_name = 'UserPost/login.html'

    def get(self, request):
        form = self.form_class(None)
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)

        if form.is_valid():

            user = form.save(commit=True)

            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user.set_password(password)
            user.save()

            user = authenticate(username=username, password=password)

            if user is not None:

                if user.is_active:
                    login(request, user)
                    return redirect('UserPost:index')

        return render(request, self.template_name, {'form': form})


def view_profile(request):
    args = {'user': request.user}
    return render(request, 'UserPost/profile.html', args)


def edit_profile(request):
    if request.method == 'POST':
        form = EditProfileForm(request.POST, instance=request.user)

        if form.is_valid():
            form.save()
            return render(request, 'UserPost/profile.html')
    else:
        form = EditProfileForm(instance=request.user)
        args = {'form': form}
        return render(request, 'UserPost/userprofile_form.html', args)


def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/UserPost/profile')
    else:
        form = RegistrationForm()

        args = {'form': form}
        return render(request, 'UserPost/reg_form.html', args)


def post_list(request):
    today = timezone.now().date()
    queryset_list = Post.objects.all()
    if request.user.is_staff or request.user.is_superuser:
        queryset = Post.objects.all()

    query = request.GET.get('q')
    if query:
        queryset_list = queryset_list.filter(
            Q(address__icontains=query) |
            Q(name__icontains=query) |
            Q(zip__icontains=query) |
            Q(city__icontains=query)
        ).distinct()
    paginator = Paginator(queryset_list, 10)
    page_request_var = "page"
    page = request.GET.get(page_request_var)
    try:
        queryset = paginator.page(page)
    except PageNotAnInteger:

        queryset = paginator.page(1)
    except EmptyPage:

            queryset = paginator.page(paginator.num_pages)

    args = {
        'object_list': queryset,
        'address': 'zip'
    }

    return render(request, 'UserPost/list.html', args)








