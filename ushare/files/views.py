from django import http
from django.utils import simplejson as json
from django.utils.decorators import method_decorator
from django.views.generic import DetailView
from django.views.generic.edit import CreateView
from django.views.decorators.csrf import csrf_exempt, csrf_protect

from .models import ImageFile
from .forms import ImageFileForm



class ImageFileCreateView(CreateView):
    form_class = ImageFileForm
    template_name = 'files/create.html'

    def form_valid(self, form):
        self.object = form.save()
        context = {
            'url': self.object.url(),
        }
        return self.get_json_response(context)

    def form_invalid(self, form):
        context = form.errors
        return self.get_json_response(context) # 409 status code?

    def get_json_response(self, context, status=200):
        content = json.dumps(context)
        return http.HttpResponse(content, 'application/json', status)


@csrf_exempt
def create_view(request, *args, **kwargs):
    view = ImageFileCreateView.as_view()
    if request.user.is_authenticated():
        view = csrf_protect(view)
    return view(request, *args, **kwargs)


class ImageFileDetailView(DetailView):
    model = ImageFile
    context_object_name = 'image'
    template_name = 'files/detail.html'
    slug_field = 'file_id'
