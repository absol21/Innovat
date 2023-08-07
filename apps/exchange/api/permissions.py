from rest_framework.permissions import BasePermission


class IsOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        owner = obj.owner
        return bool(owner == request.user)
    
    
class IsSender(BasePermission):
    def has_object_permission(self, request, view, obj):
        user = request.user
        return bool(obj.send_by == user)
    

class IsReciever(BasePermission):
    def has_object_permission(self, request, view, obj):
        user = request.user
        return bool(obj.sent_to == user)