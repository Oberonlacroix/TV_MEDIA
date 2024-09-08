from django.db import models

class Listing(models.Model):
    Start_date = models.DateField()
    Start_time = models.TimeField()
    Program_title = models.CharField(max_length=20)
    Clasification = models.CharField(max_length=100)
    Digital_EPG_synopsis = models.CharField(max_length=100)
    Episode_title = models.CharField(max_length=100)
    Major_program_genre = models.CharField(max_length=100)
    Sub_genre = models.CharField(max_length=100)
    Year_of_production = models.IntegerField()
    Actors = models.CharField(max_length=100)
    Nominal_length = models.IntegerField()
    Closed_captions = models.BooleanField(default=True)
    Premiere_episode = models.CharField(max_length=100, default='')


class Listing2(models.Model):
    Date = models.DateField()
    Time = models.TimeField()
    Name_of_program = models.CharField(max_length=100)
    Description = models.TextField()







