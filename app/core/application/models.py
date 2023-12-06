_models: list[str] = []

def register_model(model: str) -> None:
    """ Registers a model to be imported """
    _models.append(model)
    

def _get_models() -> list[str]:
    """ Returns a list of all models to be imported """
    return _models


models: list[str] = _get_models()
