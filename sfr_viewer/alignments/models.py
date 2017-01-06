from __future__ import unicode_literals

from django.db import models

class SFRPhase(models.Model):
    #an independent, individual phase of construction
    title = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=50, unique=True)
    data_directory = models.CharField(max_length=100, unique=True, default='')
    hhmodel_version = models.SlugField(max_length=100)
    cost_estimate = models.FloatField()
    flood_eliminated_parcels = models.FloatField()
    flood_improved_parcels = models.FloatField()
    flood_increased_parcels = models.FloatField()
    flood_new_parcels = models.FloatField()

    # category = models.ForeignKey('alignment.Category')

    def __str__(self):
        return self.title

# class SFRProject(models.Model):
#     #a collection of one or more implemented phases.


class Category(models.Model):
    title = models.CharField(max_length=100, db_index=True)
    slug = models.SlugField(max_length=100, db_index=True)

# SFR Program Building Block:
    #phases ar individual construction phases
    #a project is made up of one or more phases and has the option to
        #contnue to another phase
    #a program is the long term implementation of the stragetic sequence of phases
        #(a project is a state somewhere between the begining and end of the program)
