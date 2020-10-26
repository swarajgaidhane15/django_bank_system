from bank.api.views import TransactionViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('', TransactionViewSet, basename='articles')
urlpatterns = router.urls
