from django import forms
from django.utils import timezone
from .models import Event, Ticket, Review, Category


class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ('category', 'title', 'description', 'location', 'starts_at', 'capacity')
        widgets = {
            'starts_at': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'description': forms.Textarea(attrs={'rows': 4}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            existing_classes = field.widget.attrs.get('class', '')
            if isinstance(field.widget, forms.CheckboxInput):
                field.widget.attrs['class'] = (existing_classes + ' form-check-input').strip()
            else:
                field.widget.attrs['class'] = (existing_classes + ' form-control').strip()

    def clean_starts_at(self):
        starts_at = self.cleaned_data['starts_at']
        if starts_at < timezone.now():
            raise forms.ValidationError("Start date must be in the future.")
        return starts_at


class TicketForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ('seat_type',)

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ('rating', 'comment')
        widgets = {'comment': forms.Textarea(attrs={'rows': 3})}

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ('name',)
