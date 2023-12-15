from models.entity_dto import Eventos

def eventosEntity(entity) -> Eventos:
    return Eventos(**{
        **entity,
        "id": str(entity["_id"])})


def eventosList(entities) -> list[Eventos]:
    return [eventosEntity(entity) for entity in entities]