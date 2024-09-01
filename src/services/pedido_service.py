import os
import json
import boto3

from aws_lambda_powertools import Logger

class PedidoService():
    def __init__(self, logger: Logger) -> None:
        self.logger = logger
        self.url_fila_pagamentos = os.environ["url_fila_pagamentos"]
        self.sqs_client = boto3.client("sqs")
        
    def enviar_fila_pagamento(self, pedido: dict):
        self.logger.info(f"Enviando pedido {pedido['id_pedido']} para fila de pagamento.")
        
        response = self.sqs_client.send_message(QueueUrl=self.url_fila_pagamentos, MessageBody=json.dumps(pedido))
        status_code: int = response["ResponseMetadata"]["HTTPStatusCode"]
        
        self.logger.info(f"Pedido enviado para fila de pagamento: {status_code}")
        return status_code
    
    def confirmar_pagamento(self, pedido: dict):
        self.logger.info(f"Pedido {pedido['id_pedido']} confirmado. Enviando para preparação.")
