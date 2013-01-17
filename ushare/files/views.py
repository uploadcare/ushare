from django.http import HttpResponse, HttpResponsePermanentRedirect, Http404
from django.utils import simplejson as json
from django.views.generic import DetailView
from django.views.generic.edit import CreateView
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from django.utils.translation import ugettext_lazy as _

from .models import File
from .utils import decode_url



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
        return self.get_json_response(context)

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

    def get_object(self, queryset=None):
        if queryset is None:
            queryset = self.get_queryset()

        try:
            encoded_id = self.kwargs['encoded_id'] 
            obj_id = decode_url(encoded_id)
            return queryset.get(pk=obj_id)
        except (KeyError, TypeError, ValueError, File.DoesNotExist):
            raise Http404(unicode(_(u'No files found matching the query')))


class FileOEmbedView(FileDetailView):

    def render_to_response(self, *args, **kwargs):
        content = json.dumps(self.get_oembed_data())
        return HttpResponse(content, 'application/json')

    def get_oembed_data(self):
        data = self.common()
        content_type = data.get('type', u'link')
        extra_data = getattr(self, content_type)()    # TODO: Add callable() blah-blah-blah.
        data.update(extra_data)
        return data

    def common(self):
        return {
            'type': self.get_content_type(),
            'version': u'1.0',

            'title': self.object.filename,
            #'author_name': u'',
            #'author_url': u'',
            'provider_name': u'uShare',
            'provider_url': self.object.domain,
            #'cache_age': u'',
            #'thumbnail_url': u'',
            #'thumbnail_width': u'',
            #'thumbnail_height': u'',
        }

    def photo(self):
        return {
            'url': self.object.file_obj.cdn_url,
            'width': u'1000',
            'height': u'1000',
        }

    def video(self):
        return {
            'html': u'',
            'width': u'',
            'height': u'',
        }

    def link(self):
        return {}

    def rich(self):
        return {
            'html': u'',
            'width': u'',
            'height': u'',
        }

    def get_content_type(self):
        return u'photo' if self.object.is_image else u'link'

