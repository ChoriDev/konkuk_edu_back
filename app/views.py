from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from django.http import Http404
# from rest_framework import viewsets
from app.models import Item
from app.serializers import ItemSerializer
from datetime import datetime
from datetime import timedelta

# APIView로 CRUD 구현
# Item의 목록과 관련
class ItemList(APIView):
    # Item 리스트 조회
    def get(self, request):
        items = Item.objects.all()
        serializer = ItemSerializer(items, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    # 새로운 Item 추가
    def post(self, request):
        # request.data는 사용자가 보낸 데이터
        serializer = ItemSerializer(data=request.data)
        if serializer.is_valid(): # 유효성 검사
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Item의 상세 내용과 관련
class ItemDetail(APIView):
    # Item 객체 가져오기
    def get_object(self, pk):
        try:
            return Item.objects.get(pk=pk)
        except Item.DoesNotExist:
            raise Http404
    
    # Item의 상세 내용 조회
    def get(self, request, pk, format='json'):
        item = self.get_object(pk)
        serializer = ItemSerializer(item)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    # Item 수정
    def patch(self, request, pk, format='json'):
        item = self.get_object(pk)

        # 클라이언트가 보낸 데이터
        data = request.data

        if data.get('state') == True: # 물품을 대여하는 경우
            # 대여 날짜를 오늘로 지정
            data['rental_date'] = datetime.today()
            if data.get('name') == '우산': # 대여 물품이 우산인 경우
                # 대여 기간을 3일로 지정
                data['deadline_date'] = data['rental_date'] + timedelta(days=3)
            else: # 대여 물품이 그 외인 경우
                # 대여 기간을 4시간으로 지정
                data['deadline_date'] = data['rental_date'] + timedelta(hours=4)
        else: # 물품을 반납하는 경우
            data['student_id'] = None
            data['student_name'] = None
            data['rental_date'] = None
            data['deadline_date'] = None

        serializer = ItemSerializer(item, data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    # Item 삭제
    def delete(self, request, pk, format='json'):
        item = self.get_object(pk)
        item.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

# ViewSet으로 CRUD 구현
# class ItemViewSet(viewsets.ModelViewSet):
#     queryset = Item.objects.all()
#     serializer_class = ItemSerializer