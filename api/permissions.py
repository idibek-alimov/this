from rest_framework import permissions

# class BasePermission(object):
# 	"""
#      A base class form which all permission class should inherit.
# 	"""
    
#     def has_permission(self,request,view):
#     	"""
#         Return True if permissio is granted, False otherwise.
#     	"""
#         return True

#     def has_object_permission(self,request,view,obj):
#         """
#         Return Ture if permissioni sgranted ,False otherwise
#         """    
#         return Ture

class IsAuthorOrReadOnly(permissions.BasePermission):
    

    def has_object_permission(self,request,view,obj):
        #Read only permissions are allowed for any request
        if request.method in permissions.SAFE_METHODS:

            return True

        return obj.author == request.user
                    