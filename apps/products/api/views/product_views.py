from apps.base.api import GeneralListApiView
from apps.products.api.serializers.product_serializers import ProductSerializer
from rest_framework import generics, status, viewsets
from rest_framework.response import Response
from rest_framework.parsers import JSONParser, MultiPartParser

# Con el viewset haces todo el CRUD
class ProductViewSet(viewsets.ModelViewSet):
    serializer_class = ProductSerializer
    parser_classes = (JSONParser, MultiPartParser)

    def get_queryset(self, pk=None):
        if pk is None:
            return self.get_serializer().Meta.model.objects.filter(state = True)
        return self.get_serializer().Meta.model.objects.filter(state = True, id=pk).first()
    
    def list(self, request):
        # print(request.user)
        product_serializer = self.get_serializer(self.get_queryset(), many=True)
        return Response(product_serializer.data, status=status.HTTP_200_OK)

    def create(self, request):
        request.data._mutable = True # Forma BRUSCA de hacer que esto sea mutable
        data = request.data
        data['image'] = None if type(data['image']) == str else data['image']
        request.data._mutable = False
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            product = serializer.save()
            return Response({'message': 'Producto creado correctamente!', 'data':ProductSerializer(product).data}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def retrieve(self, request, pk=None):
        product = self.get_queryset(pk)
        if product:
            serializer = self.serializer_class(product)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response({'message': 'Producto no encontrado!'}, status=status.HTTP_404_NOT_FOUND)
    
    def update(self, request, pk=None):
        product = self.get_queryset(pk)
        request.data._mutable = True # Forma BRUSCA de hacer que esto sea mutable
        data = request.data
        if type(data["image"]) == str:
            del data["image"]
        request.data._mutable = False
        if product:
            product_serializer = self.serializer_class(product, data=request.data)
            if product_serializer.is_valid():
                product_serializer.save()
                return Response({'message': 'Producto actualizado!'}, status=status.HTTP_200_OK)
            return Response(product_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response({'message': 'Producto no encontrado, nada que actualizar!'}, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        product = self.get_queryset(pk)
        if product:
            product.state = False
            product.save()
            return Response({'message': 'Producto Eliminado!'}, status=status.HTTP_200_OK)
        return Response({'message': 'Producto no encontrado, nada que Eliminar!'}, status=status.HTTP_400_BAD_REQUEST)

# Asi llamas a todo un listado
class ProductListAPIView(GeneralListApiView):
    serializer_class = ProductSerializer

# Asi creas un registro
class ProductCreateAPIView(generics.CreateAPIView):
    # Ten en cuenta que se van a enviar ID si juegas con campos foraneos asi sea que se muestren los textos en el asistente.
    # A menos que especifiques en la admin de la aplicación
    serializer_class = ProductSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Producto creado correctamente!'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Asi llamas a un solo registro segun tu condicion
class ProductRetriveAPIView(generics.RetrieveAPIView):
    serializer_class = ProductSerializer
    
    # def get_queryset(self):
    #     return self.get_serializer().Meta.model.objects.filter(state = True)
    
    def get(self, request, pk):
        product = self.get_serializer().Meta.model.objects.filter(state = True).filter(id=pk).first()
        if product:
            serializer = self.serializer_class(product)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response({'message': 'Producto no encontrado!'}, status=status.HTTP_404_NOT_FOUND)

# Asi borras, y puedes personalizar para que sea borrado logico
class ProductDestroyAPIView(generics.DestroyAPIView):
    serializer_class = ProductSerializer
    
    def delete(self, request, pk):
        product = self.get_serializer().Meta.model.objects.filter(state = True).filter(id=pk).first()
        if product:
            product.state = False
            product.save()
            return Response({'message': 'Producto no Eliminado!'}, status=status.HTTP_200_OK)
        return Response({'message': 'Producto no encontrado, nada que Eliminar!'}, status=status.HTTP_400_BAD_REQUEST)

# Asi actualizas tu registro
class ProductUpdateAPIView(generics.UpdateAPIView):
    serializer_class = ProductSerializer

    def patch(self, request, pk):
        product = self.get_serializer().Meta.model.objects.filter(state = True).filter(id=pk).first()
        if product:
            product_serializer = self.serializer_class(product)
            return Response(product_serializer.data, status=status.HTTP_200_OK)
        return Response({'message': 'Producto no encontrado!'}, status=status.HTTP_400_BAD_REQUEST)
    
    def put(self, request, pk):
        product = self.get_serializer().Meta.model.objects.filter(state = True).filter(id=pk).first()
        if product:
            product_serializer = self.serializer_class(product, data=request.data)
            if product_serializer.is_valid():
                product_serializer.save()
                return Response({'message': 'Producto actualizado!'}, status=status.HTTP_200_OK)
            return Response(product_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response({'message': 'Producto no encontrado, nada que actualizar!'}, status=status.HTTP_400_BAD_REQUEST)


# Asi creas y listas al mismo tiempo, un endpoint pa list y create
class ProductListCreateAPIView(generics.ListCreateAPIView):
    serializer_class = ProductSerializer
    queryset = ProductSerializer.Meta.model.objects.filter(state = True)

    # Usa el metodo get_queryset si tu consulta tiene una logica de por medio.

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Producto creado correctamente!'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Asi puedes consultar, actualizar y eliminar un solo registro
class ProductRetrieveUpdateDestroyApiView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ProductSerializer
    
    # def get_queryset(self):
    #     return self.get_serializer().Meta.model.objects.filter(state = True)

    def get(self, request, pk):
        product = self.get_serializer().Meta.model.objects.filter(state = True).filter(id=pk).first()
        if product:
            serializer = self.serializer_class(product)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response({'message': 'Producto no encontrado!'}, status=status.HTTP_404_NOT_FOUND)
    
    def patch(self, request, pk):
        product = self.get_serializer().Meta.model.objects.filter(state = True).filter(id=pk).first()
        if product:
            product_serializer = self.serializer_class(product)
            return Response(product_serializer.data, status=status.HTTP_200_OK)
        return Response({'message': 'Producto no encontrado!'}, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk):
        product = self.get_serializer().Meta.model.objects.filter(state = True).filter(id=pk).first()
        if product:
            product_serializer = self.serializer_class(product, data=request.data)
            if product_serializer.is_valid():
                product_serializer.save()
                return Response({'message': 'Producto actualizado!'}, status=status.HTTP_200_OK)
            return Response(product_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response({'message': 'Producto no encontrado, nada que actualizar!'}, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk):
        product = self.get_serializer().Meta.model.objects.filter(state = True).filter(id=pk).first()
        if product:
            product.state = False
            product.save()
            return Response({'message': 'Producto no Eliminado!'}, status=status.HTTP_200_OK)
        return Response({'message': 'Producto no encontrado, nada que Eliminar!'}, status=status.HTTP_400_BAD_REQUEST)
        