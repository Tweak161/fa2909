from tastypie.resources import ModelResource
from results.models import Results
from tastypie.authentication import ApiKeyAuthentication


class ResultsResource(ModelResource):
    class Meta:
        queryset = Results.objects.all()
        resource_name = 'results'
        # excludes = ["id"]
        allowed_methods = ['get', 'post']
        authentication = ApiKeyAuthentication()

