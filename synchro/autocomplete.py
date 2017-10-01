from dal_select2 import views

from .models import Tag

class TagsAutocomplete(views.Select2QuerySetView):

	def get_queryset(self):
		if not self.request.user.is_authenticated():
			return Tags.objects.none()

		tags=Tag.objects.all()

		if self.q:
			tags = tags.filter(keywords__contains=self.q)

		return tags
