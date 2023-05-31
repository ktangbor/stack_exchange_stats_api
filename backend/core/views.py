from .serializers import StatResultsSerializer
from rest_framework.parsers import JSONParser
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin
from .models import Answer, StatResults
import uuid
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator


class StatResultsViewSet(
        ListModelMixin,
        RetrieveModelMixin,
        viewsets.GenericViewSet
        ):

    """
    Endpoint for getting statistics from Stack Exchange based on time period
    """

    serializer_class = StatResultsSerializer
    parser_classes = [JSONParser]

    def list(self, request):
        try:
            from_date = StatResults.date_to_epoch(date_str=request.query_params.get('since'))
            to_date = StatResults.date_to_epoch(date_str=request.query_params.get('until'))
            api_call_id = uuid.uuid4()
            StatResults.save_request_data(api_call_id, from_date, to_date)
            result = StatResults.calc_stats(api_call_id)
            result.__repr__()  # force evaluation of result
            serializer = StatResultsSerializer([result, ], many=True)

            # Clear the database
            Answer.objects.filter(api_call_id=api_call_id).delete()
            return Response(serializer.data[0])
        except Exception as e:
            return Response("Something went wrong...", status=status.HTTP_400_BAD_REQUEST)

    @method_decorator(cache_page(60 * 15))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
