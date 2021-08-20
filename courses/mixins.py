from django.http import JsonResponse
from .serializers import CreateCourseSerializer
class CourseMixin():
    template_name = 'courses/list.html'
    title = None
    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data( *args, **kwargs)
        if self.title is not None:
            context['title'] = self.title
        print(context)
        return context

    def get_queryset(self):
        return super().get_queryset().all()


class AjaxFormMixin(object):
    def form_invalid(self, form):
        response = super(AjaxFormMixin, self).form_invalid(form)
        if self.request.is_ajax():
            return JsonResponse(form.errors, status=400)
        else:
            return response

    def form_valid(self, form):
        response = super(AjaxFormMixin, self).form_valid(form)
        if self.request.is_ajax():
            
                
            data = {
                'message': "Successfully submitted form data.",
                'pk': self.object.pk
            }
            return JsonResponse(data)
        else:
            return response