# Create your views here.

from tentwatch.categories.models import ParentCategory
from sleepy.base import Base
from sleepy.responses import api_out

class CategoriesHandler(Base):
    def GET(self, request, id=None, *args, **kwargs):
        return api_out([])

class ParentCategoriesHandler(Base):
    def GET(self, request, id=None, *args, **kwargs):
        return api_out(
            [
                {
                    "name": parent.name,
                    "link": parent.get_absolute_url(),
                    "id": parent.pk,
                    "children": [
                        {
                            "name": category.name,
                            "link": category.get_absolute_url()
                            }
                        for category
                        in parent.children.all()
                        ]
                    }
                for parent
                in ParentCategory.objects.select_related().filter(visible=True).all()
                ]
            )
                    
