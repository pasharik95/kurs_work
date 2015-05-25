from tastypie.resources import ModelResource
from lots.models import *
from django.contrib.auth.models import User
from loginsys.models import *
from tastypie.authentication import Authentication
from tastypie.authorization import Authorization
from tastypie import fields
from tastypie.exceptions import *
class CorsResource(ModelResource):
    """ adds CORS headers for cross-domain requests """
    def patch_response(self, response):

        allowed_headers = ['Content-Type', 'Authorization', 'DELETE']
        response['Access-Control-Allow-Methods'] = 'get, post, DELETE, put, PUT, patch'
        response['Access-Control-Allow-Origin'] = '*'
        response['Access-Control-Allow-Headers'] = ','.join(allowed_headers)
        return response

    def dispatch(self, *args, **kwargs):
        """ calls super and patches resonse headers
            or
            catches ImmediateHttpResponse, patches headers and re-raises
        """

        try:
            response = super(CorsResource, self).dispatch(*args, **kwargs)
            return self.patch_response(response)
        except ImmediateHttpResponse, e:
            response = self.patch_response(e.response)
            # re-raise - we could return a response but then anthing wrapping
            # this and expecting an exception would be confused
            raise ImmediateHttpResponse(response)

    def method_check(self, request, allowed=None):
        """ Handle OPTIONS requests """
        if request.method.upper() == 'OPTIONS':

            if allowed is None:
                allowed = []

            allows = ','.join([s.upper() for s in allowed])

            response = HttpResponse(allows)
            response['Allow'] = allows
            raise ImmediateHttpResponse(response=response)

        return super(CorsResource, self).method_check(request, allowed)
class UserResource(ModelResource):
    class Meta:
        queryset = User.objects.all()
        resource_name = 'user'
        allowed_methods = ['get', 'post', 'delete', 'put', 'patch']
        include_resource_uri = False
        authentication = Authentication()
        authorization = Authorization()
        always_return_data = True

    def alter_list_data_to_serialize(self, request, data_dict):
        if isinstance(data_dict, dict):
            if 'meta' in data_dict:
                del(data_dict['meta'])

        return data_dict

    def obj_create(self, bundle, **kwargs):
        bundle = super(UserResource, self).obj_create(bundle, **kwargs)
        return bundle
class ProfileResource(ModelResource):

    User = fields.ForeignKey(UserResource, 'user', full=True, null=True)
    class Meta:
        queryset = Profile.objects.all()
        resource_name = 'profile'
        allowed_methods = ['get', 'post', 'delete', 'put', 'patch']
        include_resource_uri = False
        authentication = Authentication()
        authorization = Authorization()
        always_return_data = True

    def alter_list_data_to_serialize(self, request, data_dict):
        if isinstance(data_dict, dict):
            if 'meta' in data_dict:
                del(data_dict['meta'])

        return data_dict

    def obj_create(self, bundle, **kwargs):
        bundle = super(ProfileResource, self).obj_create(bundle, **kwargs)
        return bundle
class LotResource(ModelResource):

    User = fields.ForeignKey(UserResource, 'user', full=True, null=True)
    class Meta:
        queryset = Lot.objects.all()
        resource_name = 'lot'
        allowed_methods = ['get', 'post', 'delete', 'put', 'patch']
        include_resource_uri = False
        authentication = Authentication()
        authorization = Authorization()
        always_return_data = True

    def alter_list_data_to_serialize(self, request, data_dict):
        if isinstance(data_dict, dict):
            if 'meta' in data_dict:
                del(data_dict['meta'])

        return data_dict

    def obj_create(self, bundle, **kwargs):
        bundle = super(LotResource, self).obj_create(bundle, **kwargs)
        return bundle


class LikeResource(ModelResource):

    User = fields.ForeignKey(UserResource, 'user', full=True, null=True)
    Lot = fields.ForeignKey(LotResource, 'lot', full=True, null=True)
    class Meta:
        queryset = Like.objects.all()
        resource_name = 'like'
        allowed_methods = ['get', 'post', 'delete', 'put', 'patch']
        include_resource_uri = False
        authentication = Authentication()
        authorization = Authorization()
        always_return_data = True

    def alter_list_data_to_serialize(self, request, data_dict):
        if isinstance(data_dict, dict):
            if 'meta' in data_dict:
                del(data_dict['meta'])

        return data_dict

    def obj_create(self, bundle, **kwargs):
        bundle = super(LikeResource, self).obj_create(bundle, **kwargs)
        return bundle

class CommentResource(ModelResource):

    User = fields.ForeignKey(UserResource, 'user', full=True, null=True)
    Lot = fields.ForeignKey(LotResource, 'lot', full=True, null=True)
    class Meta:
        queryset = Comment.objects.all()
        resource_name = 'comment'
        allowed_methods = ['get', 'post', 'delete', 'put', 'patch']
        include_resource_uri = False
        authentication = Authentication()
        authorization = Authorization()
        always_return_data = True

    def alter_list_data_to_serialize(self, request, data_dict):
        if isinstance(data_dict, dict):
            if 'meta' in data_dict:
                del(data_dict['meta'])

        return data_dict

    def obj_create(self, bundle, **kwargs):
        bundle = super(CommentResource, self).obj_create(bundle, **kwargs)
        return bundle
class RegistrationResource(ModelResource):

    User = fields.ForeignKey(UserResource, 'user', full=True, null=True)
    Lot = fields.ForeignKey(LotResource, 'lot', full=True, null=True)
    class Meta:
        queryset = Registration.objects.all()
        resource_name = 'registration'
        allowed_methods = ['get', 'post', 'delete', 'put', 'patch']
        include_resource_uri = False
        authentication = Authentication()
        authorization = Authorization()
        always_return_data = True

    def alter_list_data_to_serialize(self, request, data_dict):
        if isinstance(data_dict, dict):
            if 'meta' in data_dict:
                del(data_dict['meta'])

        return data_dict

    def obj_create(self, bundle, **kwargs):
        bundle = super(RegistrationResource, self).obj_create(bundle, **kwargs)
        return bundle
class RateResource(ModelResource):

    User = fields.ForeignKey(UserResource, 'user', full=True, null=True)
    Lot = fields.ForeignKey(LotResource, 'lot', full=True, null=True)
    class Meta:
        queryset = Rate.objects.all()
        resource_name = 'rate'
        allowed_methods = ['get', 'post', 'delete', 'put', 'patch']
        include_resource_uri = False
        authentication = Authentication()
        authorization = Authorization()
        always_return_data = True

    def alter_list_data_to_serialize(self, request, data_dict):
        if isinstance(data_dict, dict):
            if 'meta' in data_dict:
                del(data_dict['meta'])

        return data_dict

    def obj_create(self, bundle, **kwargs):
        bundle = super(RateResource, self).obj_create(bundle, **kwargs)
        return bundle