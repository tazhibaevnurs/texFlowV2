from django import forms

from .models import Lead

_FIELD_CLASS = (
    'w-full min-h-[48px] rounded-2xl border border-slate-300 bg-white px-4 py-3 text-base '
    'text-slate-900 placeholder:text-slate-400 outline-none ring-0 transition '
    'focus:border-opal-violetdeep focus:ring-2 focus:ring-opal-violetdeep/25 '
    'dark:border-white/10 dark:bg-night-900/80 dark:text-white dark:placeholder:text-zinc-600 '
    'dark:focus:border-opal-cyan/50 dark:focus:ring-opal-cyan/20'
)
_TEXTAREA_CLASS = _FIELD_CLASS + ' min-h-[120px] resize-y'


class LeadForm(forms.ModelForm):
    class Meta:
        model = Lead
        fields = ('email', 'name', 'phone', 'employee_count', 'message')
        labels = {
            'email': 'Email',
            'name': 'Имя',
            'phone': 'Телефон',
            'employee_count': 'Количество сотрудников',
            'message': 'Сообщение',
        }
        widgets = {
            'email': forms.EmailInput(
                attrs={
                    'class': _FIELD_CLASS,
                    'placeholder': 'info@shveymetrics.kg',
                    'autocomplete': 'email',
                    'inputmode': 'email',
                }
            ),
            'name': forms.TextInput(
                attrs={
                    'class': _FIELD_CLASS,
                    'placeholder': 'Как к вам обращаться',
                    'autocomplete': 'name',
                }
            ),
            'phone': forms.TextInput(
                attrs={
                    'class': _FIELD_CLASS,
                    'placeholder': '+996 …',
                    'autocomplete': 'tel',
                }
            ),
            'employee_count': forms.NumberInput(
                attrs={
                    'class': _FIELD_CLASS,
                    'placeholder': 'Например, 25',
                    'min': 1,
                    'inputmode': 'numeric',
                }
            ),
            'message': forms.Textarea(
                attrs={
                    'class': _TEXTAREA_CLASS,
                    'placeholder': 'Кратко о цехе или задаче',
                    'rows': 4,
                }
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['email'].required = True
        self.fields['name'].required = False
        self.fields['phone'].required = False
        self.fields['employee_count'].required = False
        self.fields['message'].required = False
