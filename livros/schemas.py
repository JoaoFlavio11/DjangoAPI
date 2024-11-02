from ninja import ModelSchema, Schema
from .models import Livros

class LivrosSchema(ModelSchema):
    class Meta:
        model = Livros
        fields = ['nome', 'streaming', 'categorias']

class AvaliacaoSchema(ModelSchema):
    class Meta:
        model = Livros
        fields = ['nota','comentarios']

class FiltrosSchema(Schema):
    nota_minima: int = None
    categoriasS: int = None
    reler: bool = False