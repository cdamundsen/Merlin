from django.contrib.admin.apps import AdminConfig

class BirdsAdminConfig(AdminConfig):
    default_site = 'admin.MerlinAdminSite'