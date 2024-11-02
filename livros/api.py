from ninja import Router
from .schemas import LivrosSchema, AvaliacaoSchema
from .models import Livros, Categorias

livros_router = Router()

@livros_router.post('/')
def create_livro(request, livro_schema: LivrosSchema):
    nome = livro_schema.dict()['nome']
    streaming = livro_schema.dict()['streaming']
    categorias = livro_schema.dict()['categorias']

    if streaming not in ['F', 'AK']:
        return 400, {'status': 'ERRO: O Streaming deve ser F ou AK'}
    
    livro = Livros(
        nome=nome,
        streaming=streaming,
    )
    livro.save()

    for categoria in categorias:
        categoria_temp = Categorias.objects.get(id=categoria)
        livro.categorias.add(categoria_temp)

    return {'status': 'ok'}

@livros_router.put('/{livro_id}', response={200: dict, 400: dict, 500: dict})
def avaliar_livro(request, livro_id: int, avaliacao_schema: AvaliacaoSchema):
    comentarios = avaliacao_schema.dict().get('comentarios')
    nota = avaliacao_schema.dict().get('nota')

    try:
        livro = Livros.objects.get(id=livro_id)
        livro.comentarios = comentarios
        livro.nota = nota
        livro.save()

        return 200, {'status': 'Avaliação realizada com sucesso.'}
    except Livros.DoesNotExist:
        return 400, {'status': 'Livro não encontrado.'}
    except Exception as e:
        return 500, {'status': f'Erro interno do servidor: {str(e)}'}
    
@livros_router.delete('/{livro_id}')
def deletar_livro(request, livro_id: int):
    livro = Livros.objects.get(id=livro_id)
    livro.delete()
    
    return livro_id



