from ninja import Router

livros_router = Router()

@livros_router.post('/')
def create_livro(request):
    return {'status':'ok'}