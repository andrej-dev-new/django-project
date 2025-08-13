from django.apps import AppConfig
from django.db.models.signals import post_migrate


class AccountsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'accounts'

    def ready(self):
        post_migrate.connect(create_groups, sender=self)


def create_groups(sender, **kwargs):
    from django.contrib.auth.models import Group, Permission
    from django.contrib.contenttypes.models import ContentType
    from events.models import Event, Review

    # Create limited staff group
    staff_group, _ = Group.objects.get_or_create(name='StaffEditors')

    event_ct = ContentType.objects.get_for_model(Event)
    review_ct = ContentType.objects.get_for_model(Review)

    perms_codenames = [
        ('add_event', event_ct),
        ('change_event', event_ct),
        ('view_event', event_ct),
        ('add_review', review_ct),
        ('change_review', review_ct),
        ('view_review', review_ct),
    ]

    for codename, ct in perms_codenames:
        try:
            perm = Permission.objects.get(content_type=ct, codename=codename)
            staff_group.permissions.add(perm)
        except Permission.DoesNotExist:
            pass
