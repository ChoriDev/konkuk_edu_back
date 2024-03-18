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
        items = Item.objects.all().order_by('no')
        serializer = ItemSerializer(items, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    # 새로운 Item 추가
    def post(self, request):

        # 클라이언트가 보낸 데이터
        # QueryDict(request.data)은 immutable여서 딕셔너리로 copy
        data = request.data.copy()

        # 한 번에 물품 여러 개를 추가하는 경우
        if data.get('start_no') != "" and data.get('end_no') != "":
            # 이미 존재하는 물품인지 유효성 검사
            for no in range(int(data.get('start_no')), int(data.get('end_no')) + 1):
                item = Item.objects.filter(no=no, name=data.get('name'))
                if len(list(item)) != 0:
                    return Response(status=status.HTTP_409_CONFLICT)
            # 중복되는 물품이 없을 경우 DB에 저장
            for no in range(int(data.get('start_no')), int(data.get('end_no')) + 1):
                data['no'] = str(no)
                serializer = ItemSerializer(data=data)
                if serializer.is_valid(): # 유효성 검사
                    serializer.save()
            
            return Response(status=status.HTTP_201_CREATED)
                
        # 한 번에 물품 하나를 추가하는 경우
        else:
            serializer = ItemSerializer(data=data)
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
    def get(self, request, pk, format=None):
        item = self.get_object(pk)
        serializer = ItemSerializer(item)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    # Item 수정
    def patch(self, request, pk, format=None):
        item = self.get_object(pk)

        # 클라이언트가 보낸 데이터
        # QueryDict(request.data)은 immutable여서 딕셔너리로 copy
        data = request.data.copy()

        # 물품을 대여하는 경우
        if data.get('state') == True:
            # 대여 날짜를 오늘로 지정
            data['rental_date'] = datetime.today()
            # 대여 물품이 우산인 경우
            if data.get('name') == '우산':
                # 대여 기간을 3일로 지정
                data['deadline_date'] = data['rental_date'] + timedelta(days=3)
            # 대여 물품이 그 외인 경우
            else:
                # 대여 기간을 4시간으로 지정
                data['deadline_date'] = data['rental_date'] + timedelta(hours=4)
        # 물품을 반납하는 경우
        else:
            data['student_id'] = None
            data['student_name'] = None
            data['phone_num'] = None
            data['rental_date'] = None
            data['deadline_date'] = None

        serializer = ItemSerializer(item, data=data)

        print(data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    # Item 삭제
    def delete(self, request, pk, format=None):
        item = self.get_object(pk)
        item.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

# ViewSet으로 CRUD 구현
# class ItemViewSet(viewsets.ModelViewSet):
#     queryset = Item.objects.all()
#     serializer_class = ItemSerializer