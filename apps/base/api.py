from rest_framework import generics

# Asi optimizas algunos registros o condiciones genericas por medio de ListAPIView

class GeneralListApiView(generics.ListAPIView):

    serializer_class = None

    def get_queryset(self):
        model = self.get_serializer().Meta.model
        return model.objects.filter(state = True)