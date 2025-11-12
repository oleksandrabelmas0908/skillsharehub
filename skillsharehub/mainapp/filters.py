from django_filters import rest_framework as filters
from skillsharehub.mainapp.models import Post


class PostFilter(filters.FilterSet):
    """
    FilterSet for Post model enabling filtering by:
    - chanel: exact match by channel ID
    - chanel__name: case-insensitive partial match on channel name
    - title: case-insensitive partial match on post title
    - created_at: date range filtering (created_at__gte, created_at__lte)
    """
    chanel__name = filters.CharFilter(field_name='chanel__name', lookup_expr='icontains')
    title = filters.CharFilter(lookup_expr='icontains')
    created_at_after = filters.DateTimeFilter(field_name='created_at', lookup_expr='gte')
    created_at_before = filters.DateTimeFilter(field_name='created_at', lookup_expr='lte')

    class Meta:
        model = Post
        fields = ['chanel', 'title', 'chanel__name']
