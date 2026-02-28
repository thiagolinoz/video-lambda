#!/usr/bin/env python3
"""
Script para testar a função Lambda localmente sem AWS
"""
import json
from unittest.mock import Mock, patch


def simular_dynamodb():
    """Simula o DynamoDB com dados de teste"""
    usuarios_mock = {
        "usuario@example.com": {"email": "usuario@example.com", "senha": "senha123"},
        "teste@test.com": {"email": "teste@test.com", "senha": "test456"},
        "admin@example.com": {"email": "admin@example.com", "senha": "admin2024"}
    }
    
    def get_item_mock(Key):
        email = Key.get("email")
        if email in usuarios_mock:
            return {"Item": usuarios_mock[email]}
        return {}
    
    return get_item_mock


def executar_lambda_local(event):
    """Executa a função Lambda localmente com mock do DynamoDB"""
    with patch('lambda_handler.dynamodb') as mock_dynamodb:
        mock_table = Mock()
        mock_dynamodb.Table.return_value = mock_table
        mock_table.get_item.side_effect = lambda Key: simular_dynamodb()(Key)
        
        # Importa a função lambda após o mock estar configurado
        import lambda_handler
        
        # Executa a função
        context = {}
        response = lambda_handler.lambda_handler(event, context)
        
        return response


def main():
    print("=" * 60)
    print("TESTANDO FUNÇÃO LAMBDA LOCALMENTE")
    print("=" * 60)
    
    # Cenários de teste
    cenarios = [
        {
            "nome": "Login bem-sucedido",
            "event": {"email": "usuario@example.com", "senha": "senha123"}
        },
        {
            "nome": "Senha incorreta",
            "event": {"email": "usuario@example.com", "senha": "senhaErrada"}
        },
        {
            "nome": "Usuário não encontrado",
            "event": {"email": "naocadastrado@example.com", "senha": "senha123"}
        },
        {
            "nome": "Email ausente",
            "event": {"senha": "senha123"}
        },
        {
            "nome": "Senha ausente",
            "event": {"email": "usuario@example.com"}
        },
        {
            "nome": "Login com outro usuário",
            "event": {"email": "teste@test.com", "senha": "test456"}
        }
    ]
    
    for i, cenario in enumerate(cenarios, 1):
        print(f"\n{i}. {cenario['nome']}")
        print(f"   Event: {json.dumps(cenario['event'], indent=2)}")
        
        response = executar_lambda_local(cenario['event'])
        
        print(f"   Response:")
        print(f"   └─ Status: {response['statusCode']}")
        print(f"   └─ Body: {response['body']}")
    
    print("\n" + "=" * 60)
    print("MODO INTERATIVO")
    print("=" * 60)
    print("Digite 'sair' para encerrar\n")
    
    while True:
        try:
            email = input("Email: ").strip()
            if email.lower() == 'sair':
                break
            
            senha = input("Senha: ").strip()
            if senha.lower() == 'sair':
                break
            
            event = {"email": email, "senha": senha}
            response = executar_lambda_local(event)
            
            print(f"\n✓ Status Code: {response['statusCode']}")
            print(f"✓ Mensagem: {response['body']}\n")
            print("-" * 60)
            
        except KeyboardInterrupt:
            print("\n\nEncerrando...")
            break
        except Exception as e:
            print(f"\n✗ Erro: {e}\n")


if __name__ == "__main__":
    main()
