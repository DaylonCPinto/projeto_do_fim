# Alterações no Sistema de Validação de Formulários

## 🚨 ATENÇÃO: Após Fazer git pull

**VOCÊ PRECISA INSTALAR AS NOVAS DEPENDÊNCIAS:**
```bash
pip install -r requirements.txt
```

Se você ver este erro:
```
ModuleNotFoundError: No module named 'bleach'
```

É porque você esqueceu de executar o comando acima. Veja a seção [6. Sanitização de Dados](#6-sanitização-de-dados) para mais detalhes.

---

## Resumo das Mudanças

Este documento descreve as alterações implementadas no sistema de registro e login do Portal de Análise, conforme especificado nos requisitos.

## 1. Validação de CPF

### Backend (Python)
- **Arquivo**: `accounts/validators.py`
- **Função**: `validate_cpf(cpf)`
- Implementado algoritmo completo de validação de CPF brasileiro
- Verifica dígitos verificadores usando o algoritmo oficial
- Rejeita sequências repetidas (111.111.111-11)
- Verifica duplicatas no banco de dados

### Frontend (JavaScript)
- **Arquivo**: `static/js/form-validation.js`
- **Auto-formatação**: CPF é formatado automaticamente como XXX.XXX.XXX-XX enquanto o usuário digita
- **Bloqueio de caracteres**: Apenas números são aceitos no campo
- **Validação em tempo real**: CPF é validado ao sair do campo (blur event)

## 2. Validação de E-mail

### Domínios Permitidos
Apenas os seguintes domínios são aceitos:
- @gmail.com
- @outlook.com
- @outlook.com.br
- @hotmail.com

### Backend
- **Arquivo**: `accounts/validators.py`
- **Funções**: 
  - `validate_allowed_email_domains(email)`: Verifica domínios permitidos
  - `validate_email_characters(email)`: Valida caracteres permitidos (letras, números, ".", "-", "_")

### Frontend
- Validação em tempo real mostra mensagem sutil abaixo do campo
- Mensagem de erro clara: "Somente e-mails com os domínios @gmail.com, @outlook.com, @outlook.com.br e @hotmail.com são aceitos."

### Proteção contra Duplicatas
- E-mails duplicados são rejeitados
- Mensagem amigável sugere login ou recuperação de conta

## 3. Validação de Senha

### Requisitos
- Mínimo 8 caracteres
- Pelo menos 1 letra (maiúscula OU minúscula)
- Pelo menos 1 número
- Pelo menos 1 símbolo (!@#$%^&*(),.?":{}|<>_-+=[]\\;/`~)

### Implementação
- **Arquivo**: `accounts/password_validators.py`
- **Classe**: `CustomPasswordValidator`
- Integrado com o sistema de validação de senhas do Django
- Substitui validadores padrão no `settings.py`

### Help Text Atualizado
- "Sua senha deve ter no mínimo 8 caracteres e conter números, letras e símbolos."
- Removido: avisos redundantes sobre "campo obrigatório"

## 4. Validação de Nome de Usuário

### Requisitos
- Mínimo 8 caracteres
- Apenas letras e números (sem símbolos)
- Pelo menos 1 letra (não pode ser apenas números)

### Backend
- **Arquivo**: `accounts/validators.py`
- **Função**: `validate_username_format(username)`

### Frontend
- Validação em tempo real bloqueia símbolos
- Mensagem clara: "Apenas letras e números são permitidos."

## 5. Sistema de Login com E-mail

### Backend
- **Arquivo**: `accounts/backends.py`
- **Classe**: `EmailOrUsernameModelBackend`
- Permite login com e-mail OU nome de usuário
- Integrado no `settings.py` via `AUTHENTICATION_BACKENDS`

### Segurança
- Utiliza proteção contra timing attacks
- Compatível com o sistema de autenticação do Django

## 6. Sanitização de Dados

### Biblioteca
- **bleach**: Adicionada ao `requirements.txt`
- Sanitiza todos os campos antes da validação

### ⚠️ IMPORTANTE: Instalação
Após fazer `git pull`, **você deve instalar** a nova dependência:
```bash
pip install -r requirements.txt
```

Se você não instalar, verá o erro:
```
ModuleNotFoundError: No module named 'bleach'
```

### Campos Sanitizados
- Username
- E-mail
- CPF
- Todos os inputs são limpos de tags HTML e scripts maliciosos

## 7. Melhorias na Interface

### Help Texts Atualizados
- Removido "Obrigatório" de todos os campos
- Mantido apenas "*" para indicar campos obrigatórios
- Textos mais sutis e diretos

### Labels
- Todos os labels incluem "*" para campos obrigatórios
- Exemplo: "E-mail*", "CPF*", "Senha*"

### Mensagens de Validação
- Aparecem abaixo dos campos em tempo real
- Estilo sutil com texto pequeno
- Cor vermelha para erros
- Validação ocorre no evento "blur" (ao sair do campo)

## 8. Testes Implementados

### Arquivo
- `accounts/tests.py`

### Cobertura
- **21 testes unitários** criados
- Validação de CPF (válido, inválido, sequências)
- Validação de e-mail (domínios permitidos, caracteres)
- Validação de username (tamanho, caracteres, números)
- Validação de formulário completo
- Teste de duplicatas

### Resultado
```
Ran 21 tests in 0.366s
OK
```

## 9. Arquivos Criados/Modificados

### Novos Arquivos
1. `accounts/validators.py` - Validadores customizados
2. `accounts/password_validators.py` - Validador de senha customizado
3. `accounts/backends.py` - Backend de autenticação com e-mail
4. `static/js/form-validation.js` - Validação frontend e auto-formatação

### Arquivos Modificados
1. `accounts/forms.py` - Formulário de registro atualizado
2. `accounts/tests.py` - Testes unitários adicionados
3. `core/settings.py` - Configurações de validação e autenticação
4. `templates/registration/signup.html` - Template atualizado com JS
5. `requirements.txt` - Adicionado bleach para sanitização

## 10. Segurança

### Medidas Implementadas
- Sanitização de todos os inputs com bleach
- Validação no backend E frontend
- Proteção contra SQL injection (Django ORM)
- Proteção contra XSS (bleach + Django templates)
- CPF validado com algoritmo oficial
- Senhas fortes obrigatórias
- Verificação de duplicatas (e-mail e CPF)

## Como Testar

### 1. CPF Válido para Testes
- `111.444.777-35` (válido)
- `123.456.789-00` (inválido)

### 2. E-mails Permitidos
- usuario@gmail.com ✓
- usuario@outlook.com ✓
- usuario@outlook.com.br ✓
- usuario@hotmail.com ✓
- usuario@yahoo.com ✗

### 3. Senha Válida
- `TestPass123!` (válida)
- `testpass123` (inválida - falta símbolo)
- `TestPass` (inválida - falta número e símbolo)

### 4. Username Válido
- `testuser123` (válido)
- `test` (inválido - menos de 8 caracteres)
- `test@user` (inválido - contém símbolo)
- `12345678` (inválido - apenas números)

## Conclusão

Todas as validações foram implementadas conforme especificado:
- ✅ CPF com algoritmo de validação completo
- ✅ E-mail restrito aos domínios especificados
- ✅ Senha forte (8+ chars, letra, número, símbolo)
- ✅ Auto-formatação de CPF no frontend
- ✅ Username com mínimo 8 caracteres (letras e números)
- ✅ Login com e-mail habilitado
- ✅ Help texts atualizados (removido "Obrigatório")
- ✅ Sanitização de todos os campos
- ✅ Proteção contra duplicatas de e-mail
- ✅ Validação frontend e backend
- ✅ 21 testes unitários passando
