from django.db import models
from simple_history.models import HistoricalRecords
from apps.base.models import BaseModel

# Create your models here.
class MeasureUnit(BaseModel):
    # Model definition for MeasureUnit

    # TODO: Define fields here
    description = models.CharField('Descripción', max_length=50, blank=False, null=False, unique=True)

    class Meta:
        # Meta definition for MeasureUnit
        verbose_name = "Unidad de Medida"
        verbose_name_plural = "Unidades de Medidas"

    def __str__(self):
        return self.description
    
class CategoryProduct(BaseModel):
    # Model definition for MeasureUnit

    # TODO: Define fields here
    description = models.CharField('Descripción', max_length=50, blank=False, null=False, unique=True)

    class Meta:
        # Meta definition for MeasureUnit
        verbose_name = "Categoria de Producto"
        verbose_name_plural = "Categorias de Productos"

    def __str__(self):
        return self.description
    
class Indicator(BaseModel):
    # Model definition for Indicator

    # TODO: Define fields here
    descount_value = models.PositiveSmallIntegerField(default=0)
    category_product = models.ForeignKey(CategoryProduct, on_delete=models.CASCADE, verbose_name="Indicador de Oferta")

    class Meta:
        # Meta definition for Indicator
        verbose_name = "Indicador de Oferta"
        verbose_name_plural = "Indicadores de Ofertas"

    def __str__(self):
        return f'Oferta de la categoria {self.category_product} : {self.descount_value}%'
    
class Product(BaseModel):
    # Model definition for Indicator

    # TODO: Define fields here
    name = models.CharField('Nombre de Producto', max_length=150, unique=True, blank=False, null=False)
    description = models.TextField('Descripción de Producto', blank=False, null=False)
    image = models.ImageField('Imagen del Producto', upload_to='products/', null=True, blank = True)
    measure_unit = models.ForeignKey(MeasureUnit, on_delete=models.CASCADE, verbose_name="Unidad de Medida", null=True)
    category_product = models.ForeignKey(CategoryProduct, on_delete=models.CASCADE, verbose_name="Categoria de Producto", null=True)

    class Meta:
        # Meta definition for Indicator
        verbose_name = "Producto"
        verbose_name_plural = "Productos"

    def __str__(self):
        return self.name