# Generated migration to consolidate Exam and Mark into unified ExamMark model

import django.db.models.deletion
from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('academics', '0001_initial'),
        ('students', '0001_initial'),
        ('exams', '0003_examtype_alter_exam_exam_type'),
    ]

    operations = [
        # Step 1: Delete the Exam and Mark tables
        migrations.DeleteModel(
            name='Mark',
        ),
        migrations.DeleteModel(
            name='Exam',
        ),
        
        # Step 2: Add new fields to ExamMark
        migrations.AddField(
            model_name='exammark',
            name='exam_date',
            field=models.DateField(
                help_text='Date of the exam',
                default=django.utils.timezone.now
            ),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='exammark',
            name='exam_type',
            field=models.ForeignKey(
                help_text='Exam type (CT-Exam, Mid-Term, etc.)',
                on_delete=django.db.models.deletion.CASCADE,
                related_name='exam_marks',
                to='exams.examtype',
                null=True
            ),
        ),
        migrations.AddField(
            model_name='exammark',
            name='grade',
            field=models.CharField(
                blank=True,
                help_text='Letter grade (auto-calculated)',
                max_length=5,
                null=True
            ),
        ),
        migrations.AddField(
            model_name='exammark',
            name='remarks',
            field=models.TextField(
                blank=True,
                help_text='Teacher remarks or comments',
                null=True
            ),
        ),
        
        # Step 3: Update unique constraint
        migrations.AlterUniqueTogether(
            name='exammark',
            unique_together={('exam_type', 'exam_date', 'student', 'subject', 'session')},
        ),
        
        # Step 4: Update ordering
        migrations.AlterModelOptions(
            name='exammark',
            options={
                'indexes': [
                    models.Index(fields=['student', 'session']),
                    models.Index(fields=['exam_type', 'subject', 'session']),
                ],
                'ordering': ['-exam_date', 'student__roll_number', 'subject__name'],
                'verbose_name': 'Exam Mark',
                'verbose_name_plural': 'Exam Marks',
            },
        ),
    ]
