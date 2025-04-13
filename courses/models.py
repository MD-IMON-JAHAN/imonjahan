from django.db import models
from django.core.files.storage import FileSystemStorage

# Custom storage to handle both thumbnail folders
thumbnail_storage = FileSystemStorage(location='media/course_thumbnails')

class Course(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    duration = models.IntegerField(help_text="Duration in hours")
    thumbnail = models.ImageField(
        upload_to='course_thumbnails/',  # Consistent folder name
        null=True,
        blank=True
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    def get_thumbnail_url(self):
        if self.thumbnail and hasattr(self.thumbnail, 'url'):
            return self.thumbnail.url
        return '/static/courses/bootstrap/img/default-thumbnail.jpg'
        
    def get_absolute_url(self):
        return f"/media/{self.thumbnail}"


class Lesson(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='lessons')
    title = models.CharField(max_length=200)
    content = models.TextField()
    video_url = models.URLField(null=True, blank=True)
    completion_status = models.BooleanField(default=False)

    def __str__(self):
        return self.title

class Student(models.Model):
    name = models.CharField(max_length=200)
    email = models.EmailField(unique=True)
    enrolled_courses = models.ManyToManyField(Course, related_name='students')
    completed_lessons = models.ManyToManyField(Lesson, related_name='completed_by', blank=True)

    def __str__(self):
        return self.name



