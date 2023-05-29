from rest_framework import serializers 
from projects.models import Project, Tag, Review
from users.models import Profile


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['name', 'user', 'short_intro']

class ReviewSerializer(serializers.ModelSerializer):
    owner = ProfileSerializer(many=False)
    class Meta:
        model = Review
        fields = ['body', 'value', 'owner']

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['name']

class ProjectSerializer(serializers.ModelSerializer):
    owner = ProfileSerializer(many=False)
    tags = TagSerializer(many=True)
    reviews = serializers.SerializerMethodField()
    # since we do not have reviews field in the Project model, we can define a new attribute in this serializer class and get all the related reviews for this project
    class Meta:
        model = Project
        fields = ['title', 'description', 'owner', 'tags', 'reviews']

    def get_reviews(self, obj): # obj referes to the particular project object
        reviews = obj.review_set.all()
        serializer = ReviewSerializer(reviews, many=True)
        return serializer.data