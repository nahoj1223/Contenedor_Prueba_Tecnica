from schemas.error_schema import ErrorResponse

common_responses = {
    400: {"model": ErrorResponse, "description": "Bad request"},                
    404: {"model": ErrorResponse, "description": "Recurso no encontrado"},
    500: {"model": ErrorResponse, "description": "Error interno del servidor"}
}
