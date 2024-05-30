from apps.products.models import Product
from apps.products.api.serializers.general_serializers import MeasureUnitSerializer, CategoryProductSerializer
from rest_framework import serializers

class ProductSerializer(serializers.ModelSerializer):

    # Formas de serializar las relaciones de los modelos.

    # Metodo 1: Esta solo usala cuando el serializador sea solo para una cosa.
    # measure_unit = MeasureUnitSerializer()
    # category_product = CategoryProductSerializer()

    # Metodo 2: Asi tomara lo que referencias en el metodo __str__ del modelo 
    # measure_unit = serializers.StringRelatedField()
    # category_product = serializers.StringRelatedField()

    # Metodo 3: Usar el to_representation

    class Meta:
        model = Product
        exclude = ('state', 'created_date', 'modified_date', 'deleted_date')

    def validate_measure_unit(self, value):
        if value == "" or  value == None:
            raise serializers.ValidationError("Debe ingresar una unidad de medida")
        return value
    
    def validate_category_product(self, value):
        if value == "" or  value == None:
            raise serializers.ValidationError("Debe ingresar una categoria de producto")
        return value
    
    def validate(self, data):
        if "measure_unit" not in data.keys():
            raise serializers.ValidationError({"measure_unit":"Debe ingresar una unidad de medida"})
        
        if "category_product" not in data.keys():
            raise serializers.ValidationError({"category_product":"Debe ingresar una categoria de producto"})
        
        return data
    
    def to_representation(self, instance):
        return {
            'id': instance.id,
            'name': instance.name,
            'description': instance.description,
            'image': instance.image.url if instance.image != "" else "", # Al tratar con imagenes siempre es cadena internamente
            'measure_unit': instance.measure_unit.description if instance.measure_unit is not None else "",
            'category_product': instance.category_product.description if instance.category_product is not None else "",
        }