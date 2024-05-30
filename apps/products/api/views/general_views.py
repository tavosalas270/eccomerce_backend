from rest_framework import viewsets, status
from rest_framework.response import Response
from apps.products.api.serializers.general_serializers import MeasureUnitSerializer, IndicatorSerializer, CategoryProductSerializer

class MeasureUnitViewSet(viewsets.ModelViewSet):
    serializer_class = MeasureUnitSerializer

    def get_queryset(self, pk=None):
        if pk is None:
            return self.get_serializer().Meta.model.objects.filter(state = True)
        return self.get_serializer().Meta.model.objects.filter(state = True, id=pk).first()
    
    def create(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            all_data = self.serializer_class(self.get_queryset(), many=True).data
            return Response({'message': 'Medida creada correctamente!', 'data':all_data}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def update(self, request, pk=None):
        measure = self.get_queryset(pk)
        if measure:
            measure_serializer = self.serializer_class(measure, data=request.data)
            if measure_serializer.is_valid():
                measure_serializer.save()
                all_data = self.serializer_class(self.get_queryset(), many=True).data
                return Response({'message': 'Medida actualizada!', 'data':all_data}, status=status.HTTP_200_OK)
            return Response(measure_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response({'message': 'Medida no encontrada, nada que actualizar!'}, status=status.HTTP_400_BAD_REQUEST)
    
    def destroy(self, request, pk=None):
        measure = self.get_queryset(pk)
        if measure:
            measure.state = False
            measure.save()
            all_data = self.serializer_class(self.get_queryset(), many=True).data
            return Response({'message': 'Medida Eliminada!', 'data':all_data}, status=status.HTTP_200_OK)
        return Response({'message': 'Medida no encontrada, nada que Eliminar!'}, status=status.HTTP_400_BAD_REQUEST)
    
class CategoryProductViewSet(viewsets.ModelViewSet):
    serializer_class = CategoryProductSerializer

    def get_queryset(self, pk=None):
        if pk is None:
            return self.get_serializer().Meta.model.objects.filter(state = True)
        return self.get_serializer().Meta.model.objects.filter(state = True, id=pk).first()
    
    def create(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            all_data = self.serializer_class(self.get_queryset(), many=True).data
            return Response({'message': 'Categoria creada correctamente!', 'data':all_data}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def update(self, request, pk=None):
        category = self.get_queryset(pk)
        if category:
            category_serializer = self.serializer_class(category, data=request.data)
            if category_serializer.is_valid():
                category_serializer.save()
                all_data = self.serializer_class(self.get_queryset(), many=True).data
                return Response({'message': 'Categoria actualizada!', 'data':all_data}, status=status.HTTP_200_OK)
            return Response(category_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response({'message': 'Categoria no encontrada, nada que actualizar!'}, status=status.HTTP_400_BAD_REQUEST)
    
    def destroy(self, request, pk=None):
        category = self.get_queryset(pk)
        if category:
            category.state = False
            category.save()
            all_data = self.serializer_class(self.get_queryset(), many=True).data
            return Response({'message': 'Categoria Eliminada!', 'data':all_data}, status=status.HTTP_200_OK)
        return Response({'message': 'Categoria no encontrada, nada que Eliminar!'}, status=status.HTTP_400_BAD_REQUEST)
    
class IndicatorViewSet(viewsets.ModelViewSet):
    serializer_class = IndicatorSerializer

    def get_queryset(self, pk=None):
        if pk is None:
            return self.get_serializer().Meta.model.objects.filter(state = True, category_product__state=True)
        return self.get_serializer().Meta.model.objects.filter(state = True, id=pk, category_product__state=True).first()
    
    def create(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            all_data = self.serializer_class(self.get_queryset(), many=True).data
            return Response({'message': 'Indicador creado correctamente!', 'data':all_data}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def update(self, request, pk=None):
        indicator = self.get_queryset(pk)
        if indicator:
            indicator_serializer = self.serializer_class(indicator, data=request.data)
            if indicator_serializer.is_valid():
                indicator_serializer.save()
                all_data = self.serializer_class(self.get_queryset(), many=True).data
                return Response({'message': 'Indicador actualizado!', 'data':all_data}, status=status.HTTP_200_OK)
            return Response(indicator_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response({'message': 'Indicador no encontrado, nada que actualizar!'}, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        indicator = self.get_queryset(pk)
        if indicator:
            indicator.state = False
            indicator.save()
            all_data = self.serializer_class(self.get_queryset(), many=True).data
            return Response({'message': 'Indicador Eliminado!', 'data':all_data}, status=status.HTTP_200_OK)
        return Response({'message': 'Indicador no encontrado, nada que Eliminar!'}, status=status.HTTP_400_BAD_REQUEST)