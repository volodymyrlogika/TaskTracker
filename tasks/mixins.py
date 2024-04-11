from django.core.exceptions import PermissionDenied


class UserIsOwnerMixin(object):
    def dispatch(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.created_by != request.user:
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)


class UserIsExecutorMixin(object):
    def dispatch(self, request, *args, **kwargs):
        instance = self.get_object()
        if request.user not in instance.executors.all() or instance.created_by != request.user:
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)

