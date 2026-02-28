
import boto3

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('Usuarios')

def lambda_handler(event, context):
    email = event.get("email")
    senha = event.get("senha")

    if not email or not senha:
        return {"statusCode": 400, "body": "Email e senha obrigatórios"}

    response = table.get_item(Key={"email": email})

    if "Item" not in response:
        return {"statusCode": 404, "body": "Usuário não encontrado"}

    senha_banco = response["Item"]["senha"]

    if senha_banco == senha:
        return {"statusCode": 200, "body": "Login autorizado"}
    else:
        return {"statusCode": 401, "body": "Senha inválida"}