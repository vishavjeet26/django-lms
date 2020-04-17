from rest_framework import serializers
from library.models import Author, Books, Student, Librarian, Publisher, Issue
from django.contrib.auth.models import User
from rest_framework import permissions


class AuthorSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    firstname = serializers.CharField(required=False, allow_blank=False, max_length=100)
    lastname = serializers.CharField(required=False, allow_blank=False, max_length=100)
    dob = serializers.DateField()
    fullname = serializers.CharField(required=False, allow_blank=False, max_length=200)

    def create(self, validated_data):
        """
        Create and return a new `Author` instance, given the validated data.
        """
        return Author.objects.create(**validated_data)

    def update(self, instance, validated_data):
        """
        Update and return an existing `Author` instance, given the validated data.
        """
        instance.firstname = validated_data.get('firstname', instance.firstname)
        instance.lastname = validated_data.get('lastname', instance.lastname)
        instance.dob = validated_data.get('dob', instance.dob)
        instance.fullname = validated_data.get('fullname', instance.fullname)
        instance.save()
        return instance

class PublisherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Publisher
        fields = ['id', 'name', 'country', 'city']

class PublisherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Publisher
        fields = ['id', 'name', 'country', 'city']

class IssueSerializer(serializers.ModelSerializer):
    class Meta:
        model = Issue
        fields = ['id', 'user', 'book'] 

class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = ['id', 'user', 'enrollment_no',
        'first_name','last_name','gender','department','semester','fullname']

class LibrarianSerializer(serializers.ModelSerializer):
    class Meta:
        model = Librarian
        fields = ['id', 'user','first_name','last_name','librarian_id','fullname']

class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Books
        fields = ['book_id','title','author','isbn','publisher','due_date',
        'issue_date','return_date','request_issue','issue_status','fine','email']


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email','first_name','last_name']


