from django.http import HttpResponse, JsonResponse
from rest_framework.parsers import JSONParser
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from rest_framework import mixins
from rest_framework import generics
from django.contrib.auth.models import User
from django.db.models import Q
from django.http import Http404

# Authentication Class and function import
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework import permissions

# Custom Authentication Class and function import
from lms_api.permissions import (IsAdminOrReadOnly,IsAdminStaffOrReadOnly, 
    IsAdminStaffStudentOrReadOnly, is_admin_staff_student_user, is_admin_user,
    is_admin_staff_user, is_admin_staff_student_user)

# Custom Class and Function import
from library.models import Author, Books, Student, Librarian, Publisher, Issue, Request
from lms_api.serializers import (AuthorSerializer, PublisherSerializer, 
    IssueSerializer, StudentSerializer, LibrarianSerializer, BookSerializer,
     UserSerializer, IssueListSerializer , RequestSerializer)
from rest_framework.pagination import PageNumberPagination

class BookList(APIView):
    # List all Books, or create a new Book.
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated, IsAdminStaffOrReadOnly]
    def get(self, request, format=None):
        books = Books.objects.all()
        serializer = BookSerializer(books, many=True)
        return Response(serializer.data)
    
    # Assign book to user   
    def post(self, request, format=None):
        if not is_admin_staff_user(request):
            message = "You don't have specific permsission to access this request."
            return JsonResponse({"message": message}, status=status.HTTP_400_BAD_REQUEST)

        serializer = BookSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class BookDetail(APIView):
    """
    Retrieve, update or delete a Book instance.
    """
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated, IsAdminOrReadOnly]
    def get_object(self, pk):
        try:
            return Books.objects.get(pk=pk)
        except Books.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        book = self.get_object(pk)
        serializer = BookSerializer(book)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        if not is_admin_user(request):
            message = "You don't have specific permsission to access this request."
            return JsonResponse({"message": message}, status=status.HTTP_400_BAD_REQUEST)
        book = self.get_object(pk)
        serializer = BookSerializer(book, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        if not is_admin_user(request):
            message = "You don't have specific permsission to access this request."
            return JsonResponse({"message": message}, status=status.HTTP_400_BAD_REQUEST)
        book = self.get_object(pk)
        book.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class IssueList(APIView):
    """
    List all Issue, or create a new book issue.
    """
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated, IsAdminStaffOrReadOnly]
    def get(self, request, format=None):
        book_issues = Issue.objects.all()
        serializer = IssueListSerializer(book_issues, many=True)
        return Response(serializer.data)
    
    # Assign book to user   
    def post(self, request, format=None):
        if not is_admin_staff_user(request):
            message = "You don't have specific permsission to access this request."
            return JsonResponse({"message": message}, status=status.HTTP_400_BAD_REQUEST)
        try:
            book_id = request.data.get('book')
            book = Books.objects.get(book_id=book_id)
        except Books.DoesNotExist:
            return JsonResponse({"message": "Book is not available."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user_id = request.data.get('user')
            user = User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return JsonResponse({"message": "User is not registered."}, status=status.HTTP_400_BAD_REQUEST)

        if not book.issue_status:
            message =f"Book is not available. '{ book.title } ({ book_id })' book assign to other student"
            return JsonResponse({"message": message }, status=status.HTTP_400_BAD_REQUEST)        

        serializer = IssueSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class IssueDetail(APIView):
    """
    Retrieve, update or delete a BookIssue instance.
    """
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated, IsAdminOrReadOnly]
    def get_object(self, pk):
        try:
            return Issue.objects.get(pk=pk)
        except Issue.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        bookissue = self.get_object(pk)
        serializer = IssueListSerializer(bookissue)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        if not is_admin_staff_user(request):
            message = "You don't have specific permsission to access this request."
            return JsonResponse({"message": message}, status=status.HTTP_400_BAD_REQUEST)
        bookissue = self.get_object(pk)
        serializer = IssueSerializer(bookissue, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        if not is_admin_staff_user(request):
            message = "You don't have specific permsission to access this request."
            return JsonResponse({"message": message}, status=status.HTTP_400_BAD_REQUEST)
        bookissue = self.get_object(pk)
        bookissue.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class UserList(mixins.ListModelMixin,
                  mixins.CreateModelMixin,
                  generics.GenericAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsAdminOrReadOnly]

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

class UserDetail(mixins.RetrieveModelMixin,
                    mixins.UpdateModelMixin,
                    mixins.DestroyModelMixin,
                    generics.GenericAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly,
                      IsAdminOrReadOnly]

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)

class RequestList(generics.ListAPIView):
    queryset = Request.objects.all()
    serializer_class = RequestSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsAdminStaffStudentOrReadOnly]


class RequestDetail(generics.RetrieveAPIView):
    queryset = Request.objects.all()
    serializer_class = RequestSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly,
                      IsAdminStaffOrReadOnly]                

class AuthorList(APIView):
    # List all Books, or create a new Book.
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated, IsAdminStaffOrReadOnly]
    def get(self, request, format=None):
        author = Author.objects.all()
        serializer = AuthorSerializer(author, many=True)
        return Response(serializer.data)
       
    def post(self, request, format=None):
        if not is_admin_user(request):
            message = "You don't have specific permsission to access this request."
            return JsonResponse({"message": message}, status=status.HTTP_400_BAD_REQUEST)

        serializer = AuthorSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class AuthorDetail(APIView):
    """
    Retrieve, update or delete a Author instance.
    """
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated, IsAdminOrReadOnly]
    def get_object(self, pk):
        try:
            return Author.objects.get(pk=pk)
        except Author.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        author = self.get_object(pk)
        serializer = AuthorSerializerSerializer(author)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        if not is_admin_user(request):
            message = "You don't have specific permsission to access this request."
            return JsonResponse({"message": message}, status=status.HTTP_400_BAD_REQUEST)
        author = self.get_object(pk)
        serializer = AuthorSerializer(author, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        if not is_admin_user(request):
            message = "You don't have specific permsission to access this request."
            return JsonResponse({"message": message}, status=status.HTTP_400_BAD_REQUEST)
        author = self.get_object(pk)
        author.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class PublisherList(APIView):
    # List all Books, or create a new Book.
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated, IsAdminStaffOrReadOnly]
    def get(self, request, format=None):
        user = Publisher.objects.all()
        serializer = PublisherSerializer(user, many=True)
        return Response(serializer.data)
       
    def post(self, request, format=None):
        if not is_admin_user(request):
            message = "You don't have specific permsission to access this request."
            return JsonResponse({"message": message}, status=status.HTTP_400_BAD_REQUEST)

        serializer = PublisherSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class PublisherDetail(APIView):
    """
    Retrieve, update or delete a Publisher instance.
    """
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated, IsAdminOrReadOnly]
    def get_object(self, pk):
        try:
            return Publisher.objects.get(pk=pk)
        except Publisher.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        publisher = self.get_object(pk)
        serializer = PublisherSerializerSerializer(user)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        if not is_admin_user(request):
            message = "You don't have specific permsission to access this request."
            return JsonResponse({"message": message}, status=status.HTTP_400_BAD_REQUEST)
        publisher = self.get_object(pk)
        serializer = PublisherSerializer(publisher, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        if not is_admin_user(request):
            message = "You don't have specific permsission to access this request."
            return JsonResponse({"message": message}, status=status.HTTP_400_BAD_REQUEST)
        publisher = self.get_object(pk)
        publisher.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)



class StudentList(APIView):
    # List all Books, or create a new Book.
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated, IsAdminStaffOrReadOnly]
    def get(self, request, format=None):
        student = Student.objects.all()
        serializer = StudentSerializer(student, many=True)
        return Response(serializer.data)
       
    def post(self, request, format=None):
        if not is_admin_user(request):
            message = "You don't have specific permsission to access this request."
            return JsonResponse({"message": message}, status=status.HTTP_400_BAD_REQUEST)

        serializer = StudentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class StudentDetail(APIView):
    """
    Retrieve, update or delete a Student instance.
    """
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated, IsAdminOrReadOnly]
    def get_object(self, pk):
        try:
            return Student.objects.get(pk=pk)
        except Student.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        student = self.get_object(pk)
        serializer = StudentSerializerSerializer(student)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        if not is_admin_user(request):
            message = "You don't have specific permsission to access this request."
            return JsonResponse({"message": message}, status=status.HTTP_400_BAD_REQUEST)
        student = self.get_object(pk)
        serializer = StudentSerializer(student, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        if not is_admin_user(request):
            message = "You don't have specific permsission to access this request."
            return JsonResponse({"message": message}, status=status.HTTP_400_BAD_REQUEST)
        student = self.get_object(pk)
        student.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class LibrarianList(APIView):
    # List all Books, or create a new Book.
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated, IsAdminStaffOrReadOnly]
    def get(self, request, format=None):
        librarian = Librarian.objects.all()
        serializer = LibrarianSerializer(librarian, many=True)
        return Response(serializer.data)
       
    def post(self, request, format=None):
        if not is_admin_user(request):
            message = "You don't have specific permsission to access this request."
            return JsonResponse({"message": message}, status=status.HTTP_400_BAD_REQUEST)

        serializer = LibrarianSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LibrarianDetail(APIView):
    """
    Retrieve, update or delete a BookIssue instance.
    """
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated, IsAdminOrReadOnly]
    def get_object(self, pk):
        try:
            return Librarian.objects.get(pk=pk)
        except Librarian.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        user = self.get_object(pk)
        serializer = LibrarianSerializer(user)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        if not is_admin_user(request):
            message = "You don't have specific permsission to access this request."
            return JsonResponse({"message": message}, status=status.HTTP_400_BAD_REQUEST)
        librarian = self.get_object(pk)
        serializer = LibrarianSerializer(librarian, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        if not is_admin_user(request):
            message = "You don't have specific permsission to access this request."
            return JsonResponse({"message": message}, status=status.HTTP_400_BAD_REQUEST)
        librarian = self.get_object(pk)
        librarian.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# @api_view(['GET', 'POST'])
# @authentication_classes([SessionAuthentication, BasicAuthentication])
# @permission_classes([IsAuthenticated, IsAdminStaffOrReadOnly])
# def publisher_list(request, format=None):
#     """
#     List all code authors, or create a new authors.
#     """
#     if request.method == 'GET':
#         publishers = Publisher.objects.all()
#         serializer = PublisherSerializer(publishers, many=True)
#         return JsonResponse(serializer.data, safe=False)

#     elif request.method == 'POST':
#         data = JSONParser().parse(request)
#         serializer = PublisherSerializer(data=data)
#         if serializer.is_valid():
#             serializer.save()
#             return JsonResponse(serializer.data, status=201)
#         return JsonResponse(serializer.errors, status=400)


# @api_view(['GET', 'PUT', 'DELETE'])
# @authentication_classes([SessionAuthentication, BasicAuthentication])
# @permission_classes([IsAuthenticated, IsAdminOrReadOnly])
# def publisher_detail(request, pk, format=None):
#     """
#     Retrieve, update or delete a code publishers.
#     """
#     try:
#         publisher = Publisher.objects.get(pk=pk)
#     except Publisher.DoesNotExist:
#         return HttpResponse(status=404)

#     if request.method == 'GET':
#         serializer = PublisherSerializer(publisher)
#         return JsonResponse(serializer.data)

#     elif request.method == 'PUT':
#         data = JSONParser().parse(request)
#         serializer = PublisherSerializer(publisher, data=data)
#         if serializer.is_valid():
#             serializer.save()
#             return JsonResponse(serializer.data)
#         return JsonResponse(serializer.errors, status=400)

#     elif request.method == 'DELETE':
#         publisher.delete()
#         return HttpResponse(status=204)        






                     
