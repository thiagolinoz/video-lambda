
import boto3
import base64


dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('Persons')

def lambda_handler(event, context):

    method_arn = event["methodArn"]

    headers = {k.lower(): v for k, v in event["headers"].items()}
    auth_header = headers.get("authorization")
    print ("Authorization header:", auth_header)
    if auth_header and auth_header.startswith("Basic "):
        try:
            encoded_credentials = auth_header.split(" ")[1]

            decoded = base64.b64decode(encoded_credentials).decode("utf-8")

            email, senha = decoded.split(":")
        except:
            print('{"statusCode": 400, "body": "Credenciais inválidas"}')
            effect = "Deny"

    if email or senha:
        response = table.get_item(Key={"nmEmail": email})

        if "Item" in response:
            senha_banco = response["Item"]["cdPassword"]
            if senha_banco == senha:
                print('{"statusCode": 200, "body": "Login autorizado"}')
                effect = "Allow"
            else:
                print('{"statusCode": 401, "body": "Senha inválida"}')
                effect = "Deny"
        else:
            print('{"statusCode": 404, "body": "Usuário não encontrado"}')
            effect = "Deny"

    else:
        print ('{"statusCode": 400, "body": "Email e senha obrigatórios"}')
        effect = "Deny"
    
    return {
        "principalId": "test-user",
        "policyDocument": {
            "Version": "2012-10-17",
            "Statement": [
                {
                    "Action": "execute-api:Invoke",
                    "Effect": effect,
                    "Resource": method_arn
                }
            ]
        }
    }
##################################
########### TESTE BASE ###########
##################################

# import base64

# def lambda_handler(event, context):

#     method_arn = event["methodArn"]

#     headers = {k.lower(): v for k, v in event["headers"].items()}
#     auth_header = headers.get("authorization")
#     print ("Authorization header:", auth_header)
#     if auth_header and auth_header.startswith("Basic "):

#         encoded_credentials = auth_header.split(" ")[1]

#         decoded = base64.b64decode(encoded_credentials).decode("utf-8")

#         email, senha = decoded.split(":")

#         if (email == "certo") and (senha == "certa"):
#             print("Access granted")
#             effect = "Allow"
#         else:
#             effect = "Deny"

#     else:
#         effect = "Deny"

    
