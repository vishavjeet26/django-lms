from django.urls import path
from lms_api import views

urlpatterns = [
    path('book/', views.BookList.as_view()),
    path('book/<int:pk>/', views.BookDetail.as_view()),
    path('book-issue/', views.IssueList.as_view()),
    path('book-issue/<int:pk>/', views.IssueDetail.as_view()),
    path('author/', views.AuthorList.as_view()),
    path('author/<int:pk>/', views.AuthorDetail.as_view()),
    path('publisher/', views.PublisherList.as_view()),
    path('publisher/<int:pk>/', views.PublisherDetail.as_view()),
    path('user/', views.UserList.as_view()),
    path('user/<int:pk>/', views.UserDetail.as_view()),
    path('request/', views.RequestList.as_view()),
    path('request/<int:pk>/', views.RequestDetail.as_view()),
    path('student/', views.StudentList.as_view()),
    path('student/<int:pk>/', views.StudentDetail.as_view()),
    path('librarian/', views.LibrarianList.as_view()),
    path('librarian/<int:pk>/', views.LibrarianDetail.as_view()),
    # path('publisher/', views.publisher_list),
    # path('publisher/<int:pk>/', views.publisher_detail),

   
]