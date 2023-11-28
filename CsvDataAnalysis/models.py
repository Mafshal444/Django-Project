from mongoengine import *

# Create your models here.
class DataAnalysis(DynamicDocument):
    Id = StringField( primary_key = True )
