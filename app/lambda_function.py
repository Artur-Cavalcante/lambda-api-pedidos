import json
from aws_lambda_powertools import Logger
from aws_lambda_powertools.utilities.data_classes import event_source, APIGatewayProxyEvent

from src.services.pedido_service import PedidoService

logger = Logger(service="api-pedidos")
pedido_service = PedidoService(logger)

handlers = {
    ("POST", "/realizar_pagamento"): pedido_service.enviar_fila_pagamento
}

@event_source(data_class=APIGatewayProxyEvent)
def lambda_handler(event: APIGatewayProxyEvent, context) -> dict:
    logger.info(f"Event: {json.dumps(event)}")
    
    request = (event.http_method, event.path)
    if request in handlers:
        method = handlers[request]
        response = method(event.body)
        return response
    
    return {
        "status_code": 404,
        "body": "Método/Rota não suportado"
    }

# event = {
#     "httpMethod": "POST",
#     "path": "/realizar_pagamento",
#     "body": {
#         "id_pedido": 123,
#         "id_cliente": 456,
#         "email_cliente": "teste@mailinator.com",
#         "itens": [
#             {
#                 "nome": "hamburguer",
#                 "quantidade": 2,
#                 "valor": 40.0
#             },
#             {
#                 "nome": "refrigerante",
#                 "quantidade": 2,
#                 "valor": 8.50
#             }
#         ]
#     }
# }

# try:
#     result = lambda_handler(event, None)
#     print(result)
# except Exception as e:
#     print(f"An error occurred: {str(e)}")
