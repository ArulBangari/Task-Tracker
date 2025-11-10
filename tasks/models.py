from django.db import models

class Task(models.Model):
    # Primary key automatically created (id)
    id = models.IntegerField(primary_key=True)
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    priority = models.IntegerField(default=1)
    due_date = models.DateField(null=True, blank=True)
    user = models.CharField(max_length=255)
    completed = models.BooleanField(default=False)

    def __str__(self):
        field_values = []
        for field in self._meta.fields:
            name = field.name
            value = getattr(self, name)
            field_values.append(f"{name}: {value}")
        return ", ".join(field_values)