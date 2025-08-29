from rest_framework import serializers
from core.models import FeedBack,Student
from staff.models import Staff,Subject 


class FeedBackSeralizer(serializers.Serializer):
    student_id = serializers.IntegerField()
    feed_no = serializers.IntegerField()
    section = serializers.CharField()
    feeds = serializers.ListField(
        child=serializers.DictField()
    )
    def create(self, validated_data):
        student_id = validated_data.get('student_id')
        feeds = validated_data.get('feeds')
        section = validated_data.get('section')
        feed_no = validated_data.get('feed_no')
        #print('drf api !!')   
        feedback_objects = []

        student_instance = Student.objects.get(id=student_id)

        for feed in feeds:
            staff_id = feed['staff_id']
            subject_id = feed['subject_id']
            feedback_data = feed['feed']
            message = feed['msg']
            staff_instance = Staff.objects.get(id=staff_id)
            subject_instance = Subject.objects.get(code=subject_id)
            existing_feedback = FeedBack.objects.filter(
                student_id=student_instance.student,
                staff=staff_instance,
                subject=subject_instance,
            ).first()
            
            if feed_no == 2:
                existing_feedback.feed2 = feedback_data
                existing_feedback.msg = message  
                existing_feedback.save()
            else:
                feedback_objects.append(
                    FeedBack(
                        student=student_instance.student,
                        staff=staff_instance,
                        subject=subject_instance,
                        batch=feed['batch'],
                        dept=feed['dept'],
                        semester=feed['semester'],
                        section=section,
                        feed1=feedback_data,
                        msg=message,
                    )
                )

        return FeedBack.objects.bulk_create(feedback_objects)
