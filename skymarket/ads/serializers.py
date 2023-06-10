from rest_framework import serializers

from ads.models import Comment, Ad


class CommentSerializer(serializers.ModelSerializer):
    author_id = serializers.ReadOnlyField(source="author.id")
    author_first_name = serializers.ReadOnlyField(source="author.first_name")
    author_last_name = serializers.ReadOnlyField(source="author.last_name")
    ad_id = serializers.ReadOnlyField(source="ad.id")

    class Meta:
        fields = ["pk",
                  "text",
                  "author_id",
                  "created_at",
                  "author_first_name",
                  "author_last_name",
                  "ad_id"]
        model = Comment


class AdSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ad
        fields = ["pk", "image", "title", "price", "description"]


class AdDetailSerializer(serializers.ModelSerializer):
    author_id = serializers.ReadOnlyField(source="author.id")
    author_first_name = serializers.ReadOnlyField(source="author.first_name")
    author_last_name = serializers.ReadOnlyField(source="author.last_name")
    phone = serializers.ReadOnlyField(source="author.phone")

    class Meta:
        model = Ad
        fields = ["pk",
                  "image",
                  "title",
                  "price",
                  "phone",
                  "description",
                  "author_first_name",
                  "author_last_name",
                  "author_id"
                  ]
