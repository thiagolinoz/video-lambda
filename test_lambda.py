import pytest
from unittest.mock import Mock, patch, MagicMock
import sys


sys.modules['boto3'] = MagicMock()

import lambda_handler as lambda_module  


class TestLambdaHandler:
    """Testes unitários para a função lambda_handler"""

    @patch('lambda_handler.table')
    def test_login_bem_sucedido(self, mock_table):
        """Testa login com credenciais válidas"""
        
        mock_table.get_item.return_value = {
            "Item": {
                "email": "usuario@example.com",
                "senha": "senha123"
            }
        }
        event = {"email": "usuario@example.com", "senha": "senha123"}

       
        response = lambda_module.lambda_handler(event, {})

        
        assert response["statusCode"] == 200
        assert response["body"] == "Login autorizado"
        mock_table.get_item.assert_called_once_with(Key={"email": "usuario@example.com"})

    @patch('lambda_handler.table')
    def test_senha_invalida(self, mock_table):
        """Testa login com senha incorreta"""
        
        mock_table.get_item.return_value = {
            "Item": {
                "email": "usuario@example.com",
                "senha": "senha123"
            }
        }
        event = {"email": "usuario@example.com", "senha": "senhaErrada"}

       
        response = lambda_module.lambda_handler(event, {})

        
        assert response["statusCode"] == 401
        assert response["body"] == "Senha inválida"

    @patch('lambda_handler.table')
    def test_usuario_nao_encontrado(self, mock_table):
        """Testa login com usuário inexistente"""
        
        mock_table.get_item.return_value = {}  
        event = {"email": "inexistente@example.com", "senha": "senha123"}

        
        response = lambda_module.lambda_handler(event, {})

        
        assert response["statusCode"] == 404
        assert response["body"] == "Usuário não encontrado"

    def test_email_ausente(self):
        """Testa requisição sem email"""
        response = lambda_module.lambda_handler({"senha": "senha123"}, {})
        assert response["statusCode"] == 400
        assert response["body"] == "Email e senha obrigatórios"

    def test_senha_ausente(self):
        """Testa requisição sem senha"""
        response = lambda_module.lambda_handler({"email": "usuario@example.com"}, {})
        assert response["statusCode"] == 400
        assert response["body"] == "Email e senha obrigatórios"

    def test_email_e_senha_ausentes(self):
        """Testa requisição sem email e senha"""
        response = lambda_module.lambda_handler({}, {})
        assert response["statusCode"] == 400
        assert response["body"] == "Email e senha obrigatórios"

    def test_email_vazio(self):
        """Testa requisição com email vazio"""
        response = lambda_module.lambda_handler({"email": "", "senha": "senha123"}, {})
        assert response["statusCode"] == 400
        assert response["body"] == "Email e senha obrigatórios"

    def test_senha_vazia(self):
        """Testa requisição com senha vazia"""
        response = lambda_module.lambda_handler({"email": "usuario@example.com", "senha": ""}, {})
        assert response["statusCode"] == 400
        assert response["body"] == "Email e senha obrigatórios"
