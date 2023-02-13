from .basket import Basket

#  Context protsessorlarning vazifasi request obyektini argument sifatida qabul
# qabul qiladigan va shablon kontekstiga qo'shiladigan kalit qiymat funksyasidir

def basket(request):
    return {'basket' : Basket(request)}

