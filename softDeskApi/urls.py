from rest_framework import routers

from softDeskApi.views import ProjectListView

router = routers.SimpleRouter()
router.register('projects', ProjectListView, basename="projects")
