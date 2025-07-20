from django.contrib.admin.models import LogEntry, ADDITION, CHANGE, DELETION
from django.contrib.contenttypes.models import ContentType

def log_action(request, obj, action_flag, message=""):
    LogEntry.objects.log_action(
        user_id=request.user.pk,
        content_type_id=ContentType.objects.get_for_model(obj).pk,
        object_id=obj.pk,
        object_repr=str(obj),
        action_flag=action_flag,
        change_message=message
    )

def log_mass_action(request, action_flag, message):
    LogEntry.objects.create(
        user_id=request.user.pk,
        content_type=None,
        object_id=None,
        object_repr="-",
        action_flag=action_flag,
        change_message=message
    )
