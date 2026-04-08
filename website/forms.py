from django import forms

from .models import Lead

# Полупрозрачные поля под тёмную карточку (и при светлой ОС — без «белых пятен»)
_FIELD_CLASS = (
    'lead-form-input w-full min-h-[48px] rounded-2xl border border-white/12 bg-white/[0.06] px-4 py-3 '
    'text-base text-zinc-100 placeholder:text-zinc-500 outline-none ring-0 backdrop-blur-sm transition '
    'focus:border-opal-violetdeep focus:ring-2 focus:ring-opal-violetdeep/30 '
    'dark:border-white/10 dark:bg-night-850/70 dark:text-white dark:placeholder:text-zinc-500 '
    'dark:focus:border-opal-cyan/55 dark:focus:ring-opal-cyan/25'
)
_SELECT_CLASS = _FIELD_CLASS + ' cursor-pointer appearance-none pr-10'


class LeadForm(forms.ModelForm):
    name = forms.CharField(
        label='Имя',
        required=True,
        max_length=255,
        widget=forms.TextInput(
            attrs={
                'class': _FIELD_CLASS,
                'placeholder': 'Как к вам обращаться',
                'autocomplete': 'name',
            }
        ),
    )
    phone = forms.CharField(
        label='Телефон (WhatsApp)',
        required=True,
        max_length=64,
        widget=forms.TextInput(
            attrs={
                'class': _FIELD_CLASS,
                'placeholder': '+996 …',
                'autocomplete': 'tel',
                'inputmode': 'tel',
            }
        ),
    )

    class Meta:
        model = Lead
        fields = ('name', 'phone', 'email', 'employee_band')
        labels = {
            'email': 'Email',
            'employee_band': 'Количество сотрудников в цеху',
        }
        widgets = {
            'email': forms.EmailInput(
                attrs={
                    'class': _FIELD_CLASS,
                    'placeholder': 'name@company.kg',
                    'autocomplete': 'email',
                    'inputmode': 'email',
                }
            ),
            'employee_band': forms.Select(
                attrs={
                    'class': _SELECT_CLASS,
                }
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['email'].required = False
        self.fields['employee_band'].required = True
        self.fields['employee_band'].choices = [('', 'Выберите вариант')] + list(Lead.EmployeeBand.choices)
