from django.urls import path
from .views import (
    BoardListView,
    BoardDetailView,
    CreateBoardView,
    ListView,
    CardView,
    DeleteCardView,
    DeleteListView,
    CalendarView,
)

urlpatterns = [
    path("", BoardListView.as_view(), name="board_list"),
    path("board/<int:pk>/", BoardDetailView.as_view(), name="board_detail"),
    path("board/new/", CreateBoardView.as_view(), name="create_board"),
    path("board/<int:board_id>/list/new/", ListView.as_view(), name="create_list"),
    path("list/<int:list_id>/card/new/", CardView.as_view(), name="create_card"),
    path("card/<int:pk>/delete/", DeleteCardView.as_view(), name="delete_card"),
    path("list/<int:pk>/delete/", DeleteListView.as_view(), name="delete_list"),
    path("board/<int:pk>/calander/",CalendarView.as_view(),name = "calendar"),
]
