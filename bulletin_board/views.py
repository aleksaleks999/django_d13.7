import mimetypes

from django.contrib import messages
from django.contrib.auth.mixins import UserPassesTestMixin
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView

from bulletin_board.forms import CommentForm, AnnouncementForm
from bulletin_board.models import Announcement, Comment, AnnouncementMedia


class MyAnnouncementListView(ListView):
    model = Announcement
    context_object_name = "announcements"


class AnnouncementListView(ListView):
    model = Announcement
    context_object_name = "announcements"


class AnnouncementDetailView(DetailView):
    model = Announcement
    queryset = Announcement.objects.select_related('category', 'user').prefetch_related('announcementmedia_set')
    template_name = "bulletin_board/announcement_detail.html"
    context_object_name = "announcement"


class AnnouncementCreateView(CreateView):
    form_class = AnnouncementForm
    template_name = "bulletin_board/announcement_form.html"
    success_url = reverse_lazy("bulletin_board:announcement_list_my")

    def form_valid(self, form):
        form.instance.user = self.request.user
        ann = form.save()

        files = form.cleaned_data["media"]
        fs = FileSystemStorage()
        for f in files:
            filename = fs.save(f.name, f)
            media = AnnouncementMedia(media=filename, announcement=ann)
            media.save()

        return super().form_valid(form)


class AnnouncementUpdateView(UserPassesTestMixin, UpdateView):
    model = Announcement
    fields = "title", "text", "category", "media"
    template_name_suffix = "_update_form"

    def test_func(self):
        user = self.request.user
        obj = get_object_or_404(Announcement, pk=self.kwargs["pk"])
        return user.is_superuser or obj.user.pk == user.pk

    def get_success_url(self):
        return reverse(
            viewname="bulletin_board:announcement_detail",
            kwargs={"pk": self.object.pk},
        )


class AnnouncementDeleteView(UserPassesTestMixin, DeleteView):
    model = Announcement
    success_url = reverse_lazy("bulletin_board:announcement_list_my")
    context_object_name = "announcement"

    def test_func(self):
        user = self.request.user
        obj = get_object_or_404(Announcement, pk=self.kwargs["pk"])
        return user.is_superuser or obj.user.pk == user.pk


class CommentCreateView(CreateView):
    form_class = CommentForm
    template_name = "bulletin_board/comment_form.html"
    success_url = reverse_lazy("bulletin_board:announcement_list")

    def form_valid(self, form):
        form.instance.user = self.request.user
        announcement = get_object_or_404(Announcement, pk=self.kwargs["announcement_pk"])
        form.instance.announcement = announcement
        response = super().form_valid(form)
        return response


class CommentListView(ListView):
    queryset = Announcement.objects.filter(comment__isnull=False).prefetch_related('comment_set')
    template_name = "bulletin_board/comment_list.html"
    context_object_name = "announcements"
    

class CommentDeleteView(DeleteView):
    model = Comment
    success_url = reverse_lazy("bulletin_board:comment_list")
    context_object_name = "comment"


def comment_accept(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    comment.accepted = True
    comment.save()
    messages.success(request, 'Отклик был принят')
    return redirect('bulletin_board:comment_list')


def download_file(request):
    # fill these variables with real values
    fl_path = '/file/path'
    filename = 'downloaded_file_name.extension'
    a = request.kwargs["announcement_pk"]

    fl = open(fl_path, 'r')
    mime_type, _ = mimetypes.guess_type(fl_path)
    response = HttpResponse(fl, content_type=mime_type)
    response['Content-Disposition'] = "attachment; filename=%s" % filename
    return response
