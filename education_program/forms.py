from django import forms
from django.forms import formset_factory
from .models import EducationProgram, Professor, Institution
from django.utils.translation import gettext_lazy as _
from geopy.geocoders import Nominatim
import brazilcep
from .wiki import build_state


class EducationProgramForm(forms.ModelForm):
    class Meta:
        model = EducationProgram
        fields = ['name', 'start_date', 'end_date', 'link', 'course_type',
                  'number_students']
        widgets = {
            'course_type': forms.RadioSelect(),
            'start_date': forms.DateInput(attrs={'type': 'date', 'placeholder': 'YYYY-MM-DD'}),
            'end_date': forms.DateInput(attrs={'type': 'date', 'placeholder': 'YYYY-MM-DD'}),
            'selected_professors': forms.CheckboxSelectMultiple(attrs={'required': True})
        }


class ProfessorForm(forms.ModelForm):
    class Meta:
        model = Professor
        fields = ['name', 'username']

    def save(self, commit=True):
        name = self.cleaned_data.get('name')
        username = self.cleaned_data.get('username')

        if name and username:
            instance, created = Professor.objects.get_or_create(name=name, username=username)
        elif name:
            instance, created = Professor.objects.get_or_create(name=name)
        elif username:
            instance, created = Professor.objects.get_or_create(username=username)
        else:
            instance, created = Professor.objects.get_or_create(username="-")

        if commit:
            instance.save()

        return instance


ProfessorFormset = formset_factory(ProfessorForm, extra=1)


class InstitutionForm(forms.ModelForm):
    class Meta:
        model = Institution
        fields = ['name', 'postal_code']

    def save(self, commit=True):
        name = self.cleaned_data.get('name')
        postal_code = self.cleaned_data.get('postal_code')

        try:
            address = brazilcep.get_address_from_cep(postal_code)
            city, state = get_city_state(address)
            location = get_location_from_postal_code(f"{address['street']} - {address['city']}")
            if not location:
                location = get_location_from_postal_code(f"{address['city']}, {address['uf']}")
            lat, lon = get_coordinates(location)
        except:
            city, state, lat, lon = "", "", 0, 0

        instance, created = Institution.objects.get_or_create(name=name)

        if lat and lon:
            instance.lat = lat
            instance.lon = lon
        if city and state:
            instance.city = city
            instance.state = state
        if postal_code:
            instance.postal_code = postal_code

        if commit:
            instance.save()

        return instance


InstitutionFormset = formset_factory(InstitutionForm, extra=1)


class UpdateInstitutionForm(forms.ModelForm):
    class Meta:
        model = Institution
        fields = "__all__"

    def save(self, institution_id=None, commit=True, **kwargs):
        name = self.cleaned_data.get('name')
        postal_code = self.cleaned_data.get('postal_code')
        state = self.cleaned_data.get('state')
        city = self.cleaned_data.get('city')
        lat = self.cleaned_data.get('lat')
        lon = self.cleaned_data.get('lon')

        if institution_id:
            instance = Institution.objects.get(pk=institution_id)

            if name:
                instance.name = name
            if postal_code:
                instance.postal_code = postal_code
            if state:
                instance.state = state
            if city:
                instance.city = city
            if lat:
                instance.lat = lat
            if lon:
                instance.lon = lon

            if commit:
                instance.save()

            return instance


def get_location_from_postal_code(address):
    geolocator = Nominatim(user_agent="WikiConecta")
    location = geolocator.geocode(address, country_codes=["br"])
    return location


def get_coordinates(location):
    if location.latitude and location.longitude:
        return location.latitude, location.longitude
    else:
        return 0, 0


def get_city_state(address):
    return address["city"], address["uf"]
