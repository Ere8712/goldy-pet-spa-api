class GoldyPetSpaException(Exception):
    """Clase base para las excepciones de la API."""

    def __init__(self, message: str, status_code: int = 400):
        self.message = message
        self.status_code = status_code


class ResourceNotFoundException(GoldyPetSpaException):
    """Error cuando un recurso no existe."""

    def __init__(self, message: str = "Recurso no encontrado"):
        super().__init__(message, status_code=404)


class DuplicateResourceException(GoldyPetSpaException):
    """Error cuando ya existe un recurso."""

    def __init__(self, message: str = "El recurso ya existe"):
        super().__init__(message, status_code=400)


class BadRequestException(GoldyPetSpaException):
    """Error por solicitud inválida."""

    def __init__(self, message: str = "Solicitud inválida"):
        super().__init__(message, status_code=400)