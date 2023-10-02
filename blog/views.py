from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from .models import Post, Category, Comment, Tag, Photo
from .forms import CommentForm, PostForm, PhotoForm, ProfileForm, PasswordForm, RegistrationForm
from django.db.models import Q
from django.utils.timezone import now
from django.contrib import messages
from django.contrib.auth import logout, login
from django.http import JsonResponse, HttpResponse
from django.template.loader import render_to_string
from django.contrib.auth.models import User


# Create your views here.


def get_categories():
    all_categories = Category.objects.all()
    count = all_categories.count()
    half = count // 2
    cat1 = all_categories[:half]
    cat2 = all_categories[half:]
    return {"cat1": cat1, "cat2": cat2}


def get_tags():
    all_tags = Tag.objects.all()
    return {'all_tags': all_tags}


def tag_posts(request, name=None):
    tags = Tag.objects.all()
    tag = get_object_or_404(Tag, name=name)
    posts = Post.objects.filter(tags=tag).order_by('-published_date')
    context = {"tag": tag, "posts": posts, "tags": tags}
    context.update(get_categories())
    context.update(get_tags())
    return render(request, "blog/index.html", context=context)


def index(request):
    posts = Post.objects.all()
    context = {'posts': posts}
    context.update(get_categories())
    context.update(get_tags())
    return render(request, "blog/index.html", context=context)


def post(request, title=None):
    post = get_object_or_404(Post, title=title)
    comments = Comment.objects.filter(post=post)
    form = CommentForm()
    context = {"post": post, "comments": comments, "form": form}
    context.update(get_categories())
    context.update(get_tags())
    return render(request, "blog/post.html", context=context)


def create_comment(request):
    if request.method == "POST":
        if request.is_ajax():
            form = CommentForm(request.POST)
            if form.is_valid():
                post_id = request.POST.get('post_id')
                description = form.cleaned_data['description']
                user = request.user
                post = get_object_or_404(Post, id=post_id)

                comment = Comment.objects.create(
                    author=user,
                    description=description,
                    post=post
                )
                return JsonResponse({'error': False, 'data': comment})
    #         else:
    #             print(form.errors)
    #             return JsonResponse({'error': True, 'data': form.errors})
    #     else:
    #         error = {'message': 'Error, must be an Ajax call.'}
    #         return JsonResponse(error, content_type="application/json")
    # else:
    #     form = CommentForm()
    #     post_id = request.POST.get('post_id')
    #     post = get_object_or_404(Post, id=post_id)
    #
    #     context = {
    #         'form': form,
    #         'post':post
    #         }
    #     return render(request, template_name='post.html', context=context)

        # return redirect('post', title=post.title)


def category(request, name=None):
    c = get_object_or_404(Category, name=name)
    posts = Post.objects.filter(category=c).order_by('-published_date')
    context = {"posts": posts}
    context.update(get_categories())
    context.update(get_tags())
    return render(request, "blog/index.html", context=context)


def search(request):
    query = request.GET.get('query')
    posts = Post.objects.filter(Q(content__icontains=query) | Q(title__icontains=query))
    context = {"posts": posts}
    context.update(get_categories())
    context.update(get_tags())
    return render(request, "blog/index.html", context=context)


@login_required
def create(request):
    photos = Photo.objects.all()
    form = PostForm()
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.published_date = now()
            post.user = request.user
            post.save()
            return index(request)

    context = {'form': form, 'photos': photos}
    context.update(get_categories())
    context.update(get_tags())
    return render(request, "blog/create.html", context=context)


@login_required
def delete_post(request, post_id):
    post = get_object_or_404(Post, id=post_id, user=request.user)
    post.delete()
    return redirect('my_posts')


def my_posts(request):
    posts = Post.objects.filter(user=request.user)
    context = {'posts': posts}
    context.update(get_categories())
    context.update(get_tags())
    return render(request, 'blog/my_posts.html', context=context)



def about(request):
    return render(request, "blog/about.html")


def services(request):
    return render(request, "blog/services.html")


def contact(request):
    return render(request, "blog/contact.html")


def profile(request):
    user = request.user
    if request.method == 'POST':
        profile_form = ProfileForm(request.POST)
        if profile_form.is_valid():
            user.first_name = profile_form.cleaned_data.get('first_name')
            user.last_name = profile_form.cleaned_data.get('last_name')
            user.email = profile_form.cleaned_data.get('email')
            user.save()
            messages.success(request, 'Profile updated successfully.')
            return redirect('profile')
        else:
            messages.error(request, 'Error updating profile. Please correct the errors.')

    else:
        initial_data = {
            'first_name': user.first_name,
            'last_name': user.last_name,
            'email': user.email,
        }
        profile_form = ProfileForm(initial=initial_data)

    password_form = PasswordForm()

    if request.method == 'POST':
        password_form = PasswordForm(request.POST)
        if password_form.is_valid():
            new_password1 = password_form.cleaned_data.get('new_password1')
            new_password2 = password_form.cleaned_data.get('new_password2')
            if new_password1 == new_password2:
                user.set_password(new_password1)
                user.save()
                messages.success(request, 'Profile updated successfully.')
                return redirect('profile')
            else:
                messages.error(request, 'Error updating profile. Please correct the errors.')
    context = {'profile_form': profile_form, 'password_form': password_form}
    context.update(get_categories())
    context.update(get_tags())
    return render(request, "blog/profile.html", context=context)


def upload(request):
    form = PhotoForm()
    if request.method == 'POST':
        form = PhotoForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('main')


    return render(request, "blog/upload.html", {'form': form})

def gallery(request):
    photos = Photo.objects.all()
    contex = {'photos': photos}
    return render(request, "gallery/index.html", context=contex)

def custom_logout(request):
    logout(request)
    return redirect('main')


def registration(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('main')
    else:
        form = RegistrationForm()

    context ={'form': form}
    context.update(get_categories())
    context.update(get_tags())

    return render(request, 'blog/registration.html', context=context)
