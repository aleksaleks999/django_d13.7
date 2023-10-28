from django import forms

from bulletin_board.models import Announcement, Comment


class MultipleFileInput(forms.ClearableFileInput):
    allow_multiple_selected = True


class MultipleFileField(forms.FileField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("widget", MultipleFileInput())
        super().__init__(*args, **kwargs)

    def clean(self, data, initial=None):
        single_file_clean = super().clean
        if isinstance(data, (list, tuple)):
            result = [single_file_clean(d, initial) for d in data]
        else:
            result = single_file_clean(data, initial)
        return result


class AnnouncementForm(forms.ModelForm):
    media = MultipleFileField()

    class Meta:
        model = Announcement
        fields = "title", "text", "category"


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ("text", )
