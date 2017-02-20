from __future__ import unicode_literals
from django.db import models
from django.contrib.postgres.fields import JSONField

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

class Phase(models.Model):
    #an independent, individual phase of construction
    slug = models.SlugField(max_length=50, unique=True)
    data_directory = models.CharField(max_length=100, unique=True, default='')
    data_file = models.CharField(max_length=100, unique=True, default='')
    new_conduits = JSONField(default={})
    # parcels = JSONField(default={})
    # delta_parcels = JSONField(default={})
    cost_estimate = models.FloatField()
    parcel_hours_reduced = models.FloatField()
    parcel_hours_increased = models.FloatField()
    parcel_hours_new = models.FloatField()
    sewer_miles_new = models.FloatField()
    description = models.CharField(max_length=100)

    # def _get_efficiency(self):
    #     return self.parcel_hours_reduced / self.cost_estimate
    #
    # def _set_efficiency(self, other):
    #     inc_cost = self.cost_estimate - other.cost_estimate
    #     inc_bene = self.parcel_hours_reduced - other.parcel_hours_reduced
    #     self.efficiency = inc_bene / inc_cost

    efficiency = 0.0
    inc_cost = 0.0
    inc_bene = 0.0

    def __str__(self):
        return self.slug

class Category(models.Model):
    title = models.CharField(max_length=100, db_index=True)
    slug = models.SlugField(max_length=100, db_index=True)

# SFR Program Building Block:
    #phases ar individual construction phases
    #a project is made up of one or more phases and has the option to
        #contnue to another phase
    #a program is the long term implementation of the stragetic sequence of phases
        #(a project is a state somewhere between the begining and end of the program)
