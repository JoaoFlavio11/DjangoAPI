from ninja import Router, Query
from .schemas import LivrosSchema, AvaliacaoSchema, FiltrosSchema
from .models import Livros, Categorias

livros_router = Router()

@livros_router.post('/')
def create_livro(request, livro_schema: LivrosSchema):
    nome = livro_schema.dict().get('nome')
    streaming = livro_schema.dict().get('streaming')
    categorias = livro_schema.dict().get('categorias', [])

    if streaming not in ['F', 'AK']:
        return 400, {'status': 'ERRO: O Streaming deve ser F ou AK'}
    
    livro = Livros(
        nome=nome,
        streaming=streaming,
    )
    livro.save()

    for categoria_id in categorias:
        try:
            categoria_temp = Categorias.objects.get(id=categoria_id)
            livro.categorias.add(categoria_temp)
        except Categorias.DoesNotExist:
            return 400, {'status': f'Categoria com id {categoria_id} não encontrada.'}

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
    try:
        livro = Livros.objects.get(id=livro_id)
        livro.delete()
        return {'status': 'Livro deletado com sucesso.', 'livro_id': livro_id}
    except Livros.DoesNotExist:
        return 400, {'status': 'Livro não encontrado.'}

@livros_router.get('/sortear/')
def sortear_livro(request, filtros: Query[FiltrosSchema]):
    nota_minima = filtros.dict().get('nota_minima')
    categorias = filtros.dict().get('categorias', [])
    reler = filtros.dict().get('reler', True)

    # Garante que 'categorias' seja uma lista
    if not isinstance(categorias, list):
        categorias = [categorias]

    livros = Livros.objects.all()

    if nota_minima is not None:
        livros = livros.filter(nota__gte=nota_minima)

    if categorias:
        livros = livros.filter(categorias__id__in=categorias)

    if not reler:
        livros = livros.filter(nota=None)

    # Exemplo de retorno: sorteando um livro aleatório (substitua de acordo com a lógica necessária)
    livro_sorteado = livros.order_by('?').first() if livros.exists() else None

    if livro_sorteado:
        print(livro_sorteado)
        return {'livro_sorteado': livro_sorteado.nome}
    else:
        return {'status': 'Nenhum livro encontrado com os filtros aplicados.'}
