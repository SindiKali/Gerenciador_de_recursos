idiomas = {
    'pt': {
        'titulo': 'Gerenciador de Recursos',
        'adicionar': 'Adicionar Recurso',
        'remover': 'Remover Recurso',
        'recurso': 'Recurso',
        'lista_recursos': 'Lista de Recursos'
    },
    'ru': {
        'titulo': 'Менеджер ресурсов',
        'adicionar': 'Добавить ресурс',
        'remover': 'Удалить ресурс',
        'recurso': 'Ресурс',
        'lista_recursos': 'Список ресурсов'
    }
}

def traduzir(idioma, chave):
    return idiomas[idioma].get(chave, chave)