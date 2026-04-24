from django.contrib import admin

class MerlinAdminSite(admin.AdminSite):
    title_header = 'TenMinMerlin Admin'
    site_header = 'Ten Minute Merlin Administration'
    index_title = 'TenMinMerlin site admin'
    logout_template = 'merlin/logged_out.html'