from django import forms
from django.utils.translation import gettext as _


from .models import SupportSingle, SupportCollection


class SupportAdminForm(forms.ModelForm):
    class Meta:
        model = SupportSingle
        fields = (
            "title",
            "slug",
        )

    supports = forms.FileField(
        widget=forms.ClearableFileInput(attrs={"multiple": True}),
        label=_("Add Supports"),
        required=False,
    )

    def save_photos(self, support_single):
        """Process each uploaded image."""
        for upload in self.files.getlist("supports"):
            support = SupportCollection(support_single=support_single, supports_dir=upload)
            support.save()
