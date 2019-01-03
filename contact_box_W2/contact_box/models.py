from django.db import models
from django.urls import reverse


class Address(models.Model):
    city = models.CharField(max_length=70)
    street = models.CharField(max_length=100)
    building_number = models.PositiveIntegerField()
    apartment_number = models.PositiveIntegerField(null=True)

    class Meta:
        unique_together = ('city', 'street', 'building_number', 'apartment_number')

    def __str__(self):
        return f"{self.city} {self.street} {self.building_number} {self.apartment_number}"


class SearchPersonManager(models.Manager):
    def search(self,first_name=None, last_name=None, city=None):
        if  not city:
            return super().get_queryset().filter(first_name__icontains=first_name, last_name__icontains=last_name)
        else:
            return super().get_queryset().filter(first_name__icontains=first_name, last_name__icontains=last_name, address__city__icontains=city)


class Group(models.Model):
    group_name = models.CharField(max_length=50, unique=True)
    description = models.CharField(max_length=150, blank=True)


    def __str__(self):
        return self.group_name

    def persons_list(self):
        return [(str(p.id),str(p)) for p in self.person_set.all()]



class Person(models.Model):
    first_name = models.CharField(max_length=64)
    last_name = models.CharField(max_length=100)
    description = models.TextField()
    image = models.ImageField(null=True, blank=True, width_field='width_field', height_field='height_field')
    address = models.ForeignKey(Address, on_delete=models.SET_NULL, null=True,
                                blank=True)
    height_field = models.IntegerField(default=0, null=True, blank=True)
    width_field = models.IntegerField(default=0, null=True, blank=True)
    groups = models.ManyToManyField(Group)


    objects = models.Manager()  # The default manager.
    search_objects = SearchPersonManager()


    def __str__(self):
        return f"{self.last_name} {self.first_name}"

    def get_absolute_url(self):
        return reverse('person_details', kwargs={'id': self.id})

    def print_person_groups(self):
        return ', '.join([str(g) for g in self.groups.all()])


class PhoneNumber(models.Model):
    PHONE_TYPE = ((1, 'home'),
                  (2, 'work'),
                  (3, 'mobile'),
                  (4, 'other'))

    number = models.PositiveIntegerField(unique=True)
    type = models.SmallIntegerField(choices=PHONE_TYPE)
    person = models.ForeignKey(Person, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.number)  # nie powinno zwracac int!


class Email(models.Model):
    EMAIL_TYPE = ((1, 'private'),
                  (2, 'work'),
                  (3, 'other'))

    email = models.EmailField(unique=True)  # emailfield
    type = models.SmallIntegerField(choices=EMAIL_TYPE)
    person = models.ForeignKey(Person, on_delete=models.CASCADE)

    def __str__(self):
        return self.email



