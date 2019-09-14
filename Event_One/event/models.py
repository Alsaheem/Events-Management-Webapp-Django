from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
from PIL import Image

# Create your models here.

class Category(models.Model):
    category = models.CharField(max_length=150)

    def __str__(self):
        return '{}'.format(self.category)

class Event(models.Model):
    creator = models.ForeignKey(User,on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField()
    event_time = models.CharField(max_length=5,help_text='example 10pm , 10am.')
    location = models.CharField(max_length=300)
    category = models.ForeignKey(Category,models.CASCADE)
    google_map_link = models.CharField(max_length=255)
    event_image1 = models.ImageField(default='default.jpg' ,upload_to = 'event_images')
    event_image2 = models.ImageField(default='default.jpg' ,upload_to = 'event_images')
    event_image3 = models.ImageField(default='default.jpg' ,upload_to = 'event_images')
    created_date = models.DateTimeField(default=timezone.now)
    published_date = models.DateTimeField(blank=True, null=True)
    due_date = models.DateField(help_text='Please use the following format: <em>YYYY-MM-DD</em>.')
    claps = models.PositiveIntegerField(default=0)
    views = models.PositiveIntegerField(default=0)
    attendees = models.ManyToManyField(User, related_name='attending', blank=True)
    num_of_attendees = models.PositiveIntegerField(default=0, blank=True)
    event_notifications = models.TextField(default='')  #notification to give list of people who are attending the events

    class Meta:
        verbose_name = 'event'
        verbose_name_plural = 'events'
        ordering = ['created_date']

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        img = Image.open(self.event_image1.path)
        if img.height >301 or img.width>558:
            output_size = (558,301)
            img.thumbnail(output_size)
            img.save(self.event_image1.path)

        img2 = Image.open(self.event_image2.path)
        if img2.height >301 or img2.width>558:
            output_size = (558,301)
            img2.thumbnail(output_size)
            img2.save(self.event_image2.path)

        img3 = Image.open(self.event_image3.path)
        if img3.height >301 or img3.width>558:
            output_size = (558,301)
            img3.thumbnail(output_size)
            img3.save(self.event_image3.path)

    def get_absolute_url(self):
        return reverse("events:event_detail", kwargs={"pk": self.pk}) 

    def publish_event(self):
        self.published_date = timezone.now()
        self.save()

    def get_number_of_attendees(self):
        return self.attendees.all().count()

    def get_number_of_comments(self):
        return self.comments.all().count()

    def get_number_of_claps(self):
        return self.claps.all().count()

    def user_can_clap(self,user):
        'returns false  if user has clapped else true'
        user_claps = user.clap_set.all()
        qs = user_claps.filter(event=self)
        if qs.exists():
            return False
        else:
            return True   

    def __str__(self):
        return 'event {}- has {} views and {} claps'.format(self.title,self.views,self.claps)


class Comment(models.Model):
    event = models.ForeignKey(Event,related_name='comments',on_delete=models.CASCADE)
    author = models.ForeignKey(User,on_delete=models.CASCADE)
    comment_text = models.TextField(max_length=500)
    created_date = models.DateTimeField(default=timezone.now)

    def get_absolute_url(self):
        return reverse("event:event_detail", kwargs={"pk": self.pk}) 

    def get_comment_creator_photo(self):
        return self.author.profile.profile_pic

    def __str__(self):
        return '{}'.format(self.comment_text)

class Clap(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    event = models.ForeignKey(Event,on_delete=models.CASCADE)
    

class View(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    event = models.ForeignKey(Event,on_delete=models.CASCADE)
    
    
    




