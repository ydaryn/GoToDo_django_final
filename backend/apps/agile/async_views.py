import httpx
from adrf.views import APIView
from rest_framework.response import Response

class AsyncExternalAPIView(APIView):
    async def get(self, request):
        async with httpx.AsyncClient() as client:
            response = await client.get('https://httpbin.org/delay/1')

        return Response({
            "message": "Async I/O-bound request comleted!",
            "status_code": response.status_code
        })
