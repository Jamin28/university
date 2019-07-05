from django.contrib import admin

# Register your models here.
from myApp.models import Movie, Text, User,RtimeMovie

admin.site.register(Text)

@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):

    list_display = ['pk','name','type','country','length','release_time','score','score_num','box_office']
    list_filter = ['type']
    search_fields = ['name']
    list_per_page = 10

    fieldsets = [
        ('base',{'fields':['name','country','length','release_time']}),
        ('infer',{'fields':['type','score','score_num','box_office']})
    ]

    actions_on_bottom = True
    actions_on_top = False

@admin.register(RtimeMovie)
class RtimeMovieAdmin(admin.ModelAdmin):
    list_display = ['pk','name','link','releasetime','star','boxoffice_realtime','boxoffice_total']
    list_per_page = 5

    actions_on_bottom = True
    actions_on_top = False


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    # 进行字段重命名
    def show_pwd(self):
        return self.password1
    show_pwd.short_description = 'password'

    list_display = ['pk','username',show_pwd,'telephone']
    list_per_page = 5


    actions_on_bottom = True
    actions_on_top = False