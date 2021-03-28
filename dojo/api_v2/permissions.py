from dojo.models import Endpoint, Engagement, Product_Type, Product, Test
from django.shortcuts import get_object_or_404
from rest_framework import permissions
from dojo.authorization.authorization import user_has_permission
from dojo.authorization.roles_permissions import Permissions


def check_post_permission(request, post_model, post_pk, post_permission):
    if request.method == 'POST':
        object = get_object_or_404(post_model, pk=request.data.get(post_pk))
        return user_has_permission(request.user, object, post_permission)
    else:
        return True


def check_object_permission(request, object, get_permission, put_permission, delete_permission):
    if request.method == 'GET':
        return user_has_permission(request.user, object, get_permission)
    elif request.method == 'PUT' or request.method == 'PATCH':
        return user_has_permission(request.user, object, put_permission)
    elif request.method == 'DELETE':
        return user_has_permission(request.user, object, delete_permission)
    else:
        return False


class UserHasAppAnalysisPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        return check_post_permission(request, Product, 'product', Permissions.Product_Edit)

    def has_object_permission(self, request, view, obj):
        return check_object_permission(request, obj, Permissions.Product_View, Permissions.Product_Edit, Permissions.Product_Edit)


class UserHasEndpointPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        return check_post_permission(request, Product, 'product', Permissions.Endpoint_Add)

    def has_object_permission(self, request, view, obj):
        return check_object_permission(request, obj, Permissions.Endpoint_View, Permissions.Endpoint_Edit, Permissions.Endpoint_Delete)


class UserHasEndpointStatusPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        return check_post_permission(request, Endpoint, 'endpoint', Permissions.Endpoint_Add)

    def has_object_permission(self, request, view, obj):
        return check_object_permission(request, obj, Permissions.Endpoint_View, Permissions.Endpoint_Edit, Permissions.Endpoint_Delete)


class UserHasEngagementPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        return check_post_permission(request, Product, 'product', Permissions.Engagement_Add)

    def has_object_permission(self, request, view, obj):
        return check_object_permission(request, obj, Permissions.Engagement_View, Permissions.Engagement_Edit, Permissions.Engagement_Delete)


class UserHasFindingPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        return check_post_permission(request, Test, 'test', Permissions.Finding_Add)

    def has_object_permission(self, request, view, obj):
        return check_object_permission(request, obj, Permissions.Finding_View, Permissions.Finding_Edit, Permissions.Finding_Delete)


class UserHasProductPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        return check_post_permission(request, Product_Type, 'prod_type', Permissions.Product_Type_Add_Product)

    def has_object_permission(self, request, view, obj):
        return check_object_permission(request, obj, Permissions.Product_View, Permissions.Product_Edit, Permissions.Product_Delete)


class UserHasProductTypePermission(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method == 'POST':
            return request.user.is_staff
        else:
            return True

    def has_object_permission(self, request, view, obj):
        return check_object_permission(request, obj, Permissions.Product_Type_View, Permissions.Product_Type_Edit, Permissions.Product_Type_Delete)


class UserHasTestPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        return check_post_permission(request, Engagement, 'engagement', Permissions.Test_Add)

    def has_object_permission(self, request, view, obj):
        return check_object_permission(request, obj, Permissions.Test_View, Permissions.Test_Edit, Permissions.Test_Delete)


class UserHasTestImportPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        return check_post_permission(request, Test, 'test', Permissions.Test_Edit)

    def has_object_permission(self, request, view, obj):
        return check_object_permission(request, obj, Permissions.Test_View, Permissions.Test_Edit, Permissions.Test_Delete)


class IsSuperUser(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_superuser
