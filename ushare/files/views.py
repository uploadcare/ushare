from django.views.generic import DetailView
from django.views.generic.edit import CreateView

from .models import ImageFile
from forms import ImageFileForm



class ImageFileCreateView(CreateView):
    form_class = ImageFileForm
    template_name = 'files/create.html'

    def form_valid(self, form):
        return super(ImageFileCreateView, self).form_valid(form)

    def form_invalid(self, form):
        return super(ImageFileCreateView, self).form_invalid(form)

index = ImageFileCreateView.as_view()


class ImageFileDetailView(DetailView):
    model = ImageFile
    context_object_name = 'image'
    template_name = 'files/detail.html'
