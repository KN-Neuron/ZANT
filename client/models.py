from django.db import models
from django.urls import reverse

class Address(models.Model):
    """Address model"""

#     # Fields
#     street = models.CharField(verbose_name="Ulica")
#     house_number = models.CharField(verbose_name="Numer domu")
#     flat_number = models.CharField(verbose_name="Numer mieszkania")
#     city_code = models.CharField(verbose_name="Kod pocztowy")
#     city = models.CharField(verbose_name="Miasto")
#     district = models.CharField(verbose_name="Gmina/Dzielnica")
#     country = models.CharField(verbose_name="Państwo")

# class AccidentReport(models.Model):
#     """Accident report model"""

#     # Victim's personal data
#     id_number = models.CharField(verbose_name="Numer PESEL (lub dokumentu tożsamości)")
#     name = models.CharField(verbose_name="Imię")
#     surname = models.CharField(verbose_name="Nazwisko")
#     dob = models.DateField(verbose_name="Data urodzenia")
#     sex = models.CharField(verbose_name="Płeć")
#     birthplace = models.CharField(verbose_name="Miejsce urodzenia")

#     # Victim's address
#     victim_address = models.OneToOneField(Address, on_delete=models.CASCADE, verbose_name="Adres zamieszkania")

#     # Correspondence address
#     correspondence_address = models.OneToOneField(Address, on_delete=models.CASCADE, verbose_name="Adres do korespondencji")

    # # Metadata
    # class Meta:
    #     ordering = ['-my_field_name']

    # Methods
    def get_absolute_url(self):
        """Returns the URL to access a particular instance of MyModelName."""
        return reverse('model-detail-view', args=[str(self.id)])

    def __str__(self):
        """String for representing the MyModelName object (in Admin site etc.)."""
        return self.my_field_name

class VictimReport(models.Model):
    """Victim report model"""

    # Fields

