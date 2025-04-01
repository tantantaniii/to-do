from django.db import models

class Task(models.Model):
    title = models.CharField(max_length=200)
    complition = models.BooleanField(default=False)
    tag = models.ManyToManyField('Tag')
    def __str__(self):
        return self.title
    # def dict_result(self):
    #     result = {
    #         "id": self.id,
    #         "title": self.title,
    #         "comptltion": self.complition
    #     }
    #     return result
class Tag(models.Model):
    name = models.CharField(max_length=200)
    def __str__(self):
        return self.name


