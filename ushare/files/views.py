from django.http import HttpResponse, HttpResponsePermanentRedirect
from django.utils import simplejson as json
from django.views.generic import DetailView
from django.views.generic.edit import CreateView
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt, csrf_protect

from .models import File



class FileCreateView(CreateView):
    model = File
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
        return HttpResponse(content, 'application/json', status)

    def get_context_data(self, *args, **kwargs):
        context = super(FileCreateView, self).get_context_data(*args, **kwargs)
        context.update({
            'ALLOWED_EXTENSIONS': getattr(settings, 'ALLOWED_EXTENSIONS', ()),
            'FORBIDDEN_EXTENSIONS': getattr(settings, 'FORBIDDEN_EXTENSIONS', ()),
            'MAX_FILE_SIZE': getattr(settings, 'MAX_FILE_SIZE', 100 * 1024 * 1024),
        })
        return context


@csrf_exempt
def create_view(request, *args, **kwargs):
    view = FileCreateView.as_view()
    if request.user.is_authenticated():
        view = csrf_protect(view)
    return view(request, *args, **kwargs)


class FileDetailView(DetailView):
    model = File
    context_object_name = 'file'
    template_name = 'files/detail.html'
    slug_field = 'file_id'
