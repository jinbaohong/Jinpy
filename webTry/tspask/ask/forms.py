from django import forms
 
class tryForm(forms.Form):
	companyName = forms.CharField()
	contact = forms.CharField()
    phone = forms.CharField()
    name = forms.CharField()
    # url = forms.URLField()
    choice_export = (('yes', 'yes'), ('no', 'no'),)
    isExport = forms.ChoiceField(choices=choice_export)
	choice_planToExhibit = (('yes', 'yes'), ('no', 'no'))
    planToExhibit = forms.ChoiceField(choices=choice_planToExhibit)
	choice_planToExhibit = (('yes', 'yes'), ('no', 'no'))
    say = forms.CharField(
        max_length=2000,
        widget=forms.Textarea(),
        help_text='Write here your message!'
    )
