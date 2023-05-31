from django.db import models
from utils.model_abstracts import Model
import uuid
from django.db.models import JSONField
from datetime import datetime
import requests
import json
from django.db.models import Count, Avg


class Answer(
    Model
):

    class Meta:
        verbose_name = 'Answer'
        verbose_name_plural = "Answers"
        ordering = ["answer_id"]

    answer_id = models.IntegerField(default=0)
    is_accepted = models.BooleanField()
    score = models.IntegerField(default=0)
    question_id = models.IntegerField(default=0)
    api_call_id = models.UUIDField(default=uuid.uuid4)  # unique id for api call, in case of simultaneous calls

    def __str__(self):
        return str(self.answer_id)


class Comment(
    Model
):

    class Meta:
        verbose_name = 'Comment'
        verbose_name_plural = "Comments"
        ordering = ["comment_id"]

    comment_id = models.IntegerField(default=0)
    post_id = models.ForeignKey(Answer, on_delete=models.CASCADE)
    api_call_id = models.UUIDField(default=uuid.uuid4)  # unique id for api call, in case of simultaneous calls

    def __str__(self):
        return str(self.comment_id)


class StatResults(
    Model
):

    class Meta:
        verbose_name = 'StatResults'
        verbose_name_plural = "StatResults"
        ordering = ["total_accepted_answers"]

    total_accepted_answers = models.IntegerField(default=0)
    accepted_answers_average_score = models.FloatField(default=0.00)
    average_answers_per_question = models.FloatField(default=0.00)
    top_ten_answers_comment_count = JSONField()

    @staticmethod
    def date_to_epoch(date_str):
        return int(datetime.strptime(date_str, '%Y-%m-%d %H:%M:%S').timestamp())

    @staticmethod
    def get_answer_data(from_date, to_date):
        answers_url = f'https://api.stackexchange.com/2.3/answers?pagesize=100&fromdate={from_date}&' \
                      f'todate={to_date}&order=desc&sort=activity&site=stackoverflow'
        response = requests.get(answers_url)
        return json.loads(response.text)

    @staticmethod
    def get_comments_data(answer_ids):
        comments_url = f'https://api.stackexchange.com/2.3/answers/{answer_ids}/comments?pagesize=100&' \
                       'order=desc&sort=creation&site=stackoverflow'
        response = requests.get(comments_url)
        return json.loads(response.text)

    @staticmethod
    def save_request_data(api_call_id, from_date, to_date):
        # save answers
        answers_data = StatResults.get_answer_data(from_date, to_date)
        answer_ids = ''  # collect the answer ids for faster comments collection
        answers = {}
        for answ in answers_data["items"]:
            answer = Answer()
            answer.is_accepted = answ['is_accepted']
            answer.answer_id = int(answ['answer_id'])
            answer.score = int(answ['score'])
            answer.question_id = answ['question_id']
            answer.api_call_id = api_call_id
            answer.save()
            answer_ids += str(answer.answer_id) + ';'  # collect the ids for the api call
            answers[answer.answer_id] = answer
        answer_ids = answer_ids[:-1]  # remove trailing ';'

        # save comments of above answers
        comments_data = StatResults.get_comments_data(answer_ids)
        for comm in comments_data["items"]:
            comment = Comment()
            comment.comment_id = str(comm['comment_id'])
            comment.post_id = answers[int(comm['post_id'])]
            comment.api_call_id = api_call_id
            comment.save()

    @staticmethod
    def calc_stats(api_call_id):
        total_accepted_answers = Answer.objects.filter(api_call_id=api_call_id, is_accepted=True).count()
        accepted_answers_average_score = (Answer.objects.filter(api_call_id=api_call_id, is_accepted=True)
                                          .aggregate(Avg('score')))['score__avg']
        average_answers_per_question = (Answer.objects.filter(api_call_id=api_call_id).values('question_id')
                                        .annotate(countA=Count('answer_id'))
                                        .order_by().aggregate(Avg('countA')))['countA__avg']
        top_ten_answers = (Answer.objects.filter(api_call_id=api_call_id).values('answer_id').order_by('-score')[:10]) \
            .annotate(comment_count=Count('comment'))
        top_ten_answers_comment_count = {it['answer_id']: it['comment_count'] for it in top_ten_answers}

        result = StatResults()
        result.total_accepted_answers = int(total_accepted_answers)
        result.accepted_answers_average_score = round(float(accepted_answers_average_score), 2)
        result.average_answers_per_question = round(float(average_answers_per_question), 1)
        result.top_ten_answers_comment_count = top_ten_answers_comment_count

        return result

    def __str__(self):
        return str(self.total_accepted_answers)

