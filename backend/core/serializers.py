from rest_framework_json_api import serializers
from . import models


class AnswerSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Answer
        fields = ('answer_id', 'is_accepted', 'score', 'question_id', 'api_call_id', )

    def validate(self, attrs):
        pass


class CommentSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Comment
        fields = ('comment_id', 'post_id', 'api_call_id', )

    def validate(self, attrs):
        pass


class StatResultsSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.StatResults
        fields = ('total_accepted_answers', 'accepted_answers_average_score', 'average_answers_per_question',
                  'top_ten_answers_comment_count',)

    def validate(self, attrs):
        pass

