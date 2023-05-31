# Generated by Django 4.1.3 on 2023-05-29 10:11

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Answer',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('answer_id', models.IntegerField(default=0)),
                ('is_accepted', models.BooleanField()),
                ('score', models.IntegerField(default=0)),
                ('question_id', models.IntegerField(default=0)),
                ('api_call_id', models.UUIDField(default=uuid.uuid4)),
            ],
            options={
                'verbose_name': 'Answer',
                'verbose_name_plural': 'Answers',
                'ordering': ['answer_id'],
            },
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('comment_id', models.IntegerField(default=0)),
                ('api_call_id', models.UUIDField(default=uuid.uuid4)),
                ('post_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.answer')),
            ],
            options={
                'verbose_name': 'Comment',
                'verbose_name_plural': 'Comments',
                'ordering': ['comment_id'],
            },
        ),
    ]