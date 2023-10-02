from django.shortcuts import render, redirect
from .models import Photo
from .forms import PhotoForm

# Create your views here.

def gallery(request):
    photos = Photo.objects.all()
    contex = {'photos': photos}
    return render(request, "gallery/index.html", context=contex)


def upload(request):
    form = PhotoForm()
    if request.method == 'POST':
        form = PhotoForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('gallery')

    return render(request, "gallery/upload.html", {'form': form})