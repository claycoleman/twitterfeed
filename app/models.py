from django.db import models

# Create your models here.
class Tweet(models.Model):
    """
    Description: Model Description
    """
    screen_name = models.CharField(max_length=255, null=True, blank=True)
    created_at = models.CharField(max_length=255, null=True, blank=True)
    inserted_to_database_at = models.DateTimeField(null=True, blank=True, auto_now=True)
    location = models.CharField(max_length=250, null=True, blank=True)
    profile_image = models.ImageField(upload_to="profile_images", null=True, blank=True)
    text = models.TextField(null=True, blank=True)
    trend = models.ForeignKey('Trend', null=True, blank=True)
    tweet_id = models.CharField(null=True, blank=True, max_length=255)


    class Meta:
        ordering = ['-inserted_to_database_at']


class Location(models.Model):
    name = models.CharField(null=True, blank=True, max_length=255)
    woeid = models.IntegerField(null=True, blank=True)
    slug = models.SlugField(null=True, blank=True)
    coords = models.TextField(null=True, blank=True)
    place_id = models.CharField(max_length=255, null=True, blank=True)

    def saveSlug(self):
        self.slug = self.name.replace(" ", "-").lower()

    # def save(self, *args, **kwargs):
    #     if self.name != None:
    #         self.slug = self.name.replace(" ", "-").lower()
    #     super(Location, self).save(*args, **kwargs)



class Trend(models.Model):
    """
    Description: Model Description
    """
    name = models.CharField(null=True, blank=True, max_length=255)
    query = models.CharField(null=True, blank=True, max_length=255)
    url = models.URLField(null=True, blank=True)
    location = models.ManyToManyField('Location', blank=True)
    inserted_to_database_at = models.DateTimeField(null=True, blank=True, auto_now=True)
    slug = models.SlugField(null=True, blank=True)

    def __unicode__(self):
            return self.name

    def saveSlug(self):
        self.slug = self.name.replace(" ", "-").lower()[:15]