# from django.db import models

# class ObjectIdField(models.Field):
#     description = "A field that stores MongoDB's ObjectId."

#     def __init__(self, *args, **kwargs):
#         kwargs.setdefault('editable', False)
#         kwargs.setdefault('primary_key', True)
#         kwargs.setdefault('max_length', 24)
#         super().__init__(*args, **kwargs)

#     def db_type(self, connection):
#         return 'ObjectId'
