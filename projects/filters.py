import django_filters
from django.db.models import Q 


class ProjectFilter(django_filters.FilterSet):
    search = django_filters.CharFilter(method='search_projects', label='Search') 

    def search_projects(self, queryset, name, value):
        return queryset.distinct().filter(
            Q(title__icontains = value) |
            Q(description__icontains=value) |
            Q(owner__username__icontains=value) |
            Q(owner__name__icontains=value) |
            Q(tags__name__icontains=value)
        )
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.filters['search'].field.widget.attrs.update({'class': 'input input--text', 'placeholder': 'Search Projects'})