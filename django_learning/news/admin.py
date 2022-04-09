from django.contrib import admin
from django import forms
from django.utils.safestring import mark_safe
from ckeditor_uploader.widgets import CKEditorUploadingWidget

from .models import News, Category

class NewsAdminForm(forms.ModelForm):
    content = forms.CharField(widget=CKEditorUploadingWidget())
    # prepopulated_fields = {'slug':('title',)}
    class Meta:
        model = News
        fields = '__all__'

class NewsAdmin(admin.ModelAdmin):

    form = NewsAdminForm

    list_display = ('id','title','category','created_at','updated_at','is_published','get_photo')
    list_display_links = ('id','title')
    search_fields = ('title','content')
    list_editable = ('is_published',)
    list_filter = ('is_published','category')
    fields = ('title','category','content','photo','get_photo','is_published','views','created_at','updated_at')
    readonly_fields = ('get_photo','views','created_at','updated_at')
    save_on_top = True
    # prepopulated_fields = {'slug':('title',)}
    


    def get_photo(self, obj):
        if obj.photo:
            return mark_safe(f'<img src="{obj.photo.url}" width="30">')

    get_photo.short_description = 'photo'

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id','title')
    list_display_links = ('id','title')
    search_fields = ('title',)
    prepopulated_fields = {'slug':('title',)}


admin.site.register(News, NewsAdmin)
admin.site.register(Category, CategoryAdmin)

admin.site.site_title='News control'
admin.site.site_header='News control'
