from django.urls import path

from bulletin_board.views import AnnouncementListView, MyAnnouncementListView, AnnouncementCreateView, \
    AnnouncementUpdateView, AnnouncementDetailView, CommentListView, AnnouncementDeleteView, \
    CommentCreateView, comment_accept, download_file, CommentDeleteView

app_name = "bulletin_board"


urlpatterns = [
    path("announcements", AnnouncementListView.as_view(), name="announcement_list"),
    path("announcements/my", MyAnnouncementListView.as_view(), name="announcement_list_my"),
    path("announcements/create", AnnouncementCreateView.as_view(), name="announcement_create"),
    path("announcements/<int:pk>/update/", AnnouncementUpdateView.as_view(), name="announcement_update"),
    path("announcements/<int:pk>/", AnnouncementDetailView.as_view(), name="announcement_detail"),
    path("announcements/<int:pk>/delete", AnnouncementDeleteView.as_view(), name="announcement_delete"),

    path("announcements/<int:announcement_pk>/comment", CommentCreateView.as_view(), name="comment_create"),

    path("comments", CommentListView.as_view(), name="comment_list"),
    path("comments/<int:pk>/accept", comment_accept, name="comment_accept"),
    path("comments/<int:pk>/delete", CommentDeleteView.as_view(), name="comment_delete"),

    path('media/<str:filepath>', download_file, name="download_file")
]
