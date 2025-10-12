# 🔧 Fix: ModuleNotFoundError: No module named 'bleach'

## O Problema

Após fazer `git pull`, você está vendo este erro:

```
ModuleNotFoundError: No module named 'bleach'
```

ao executar comandos como:
- `python manage.py makemigrations`
- `python manage.py migrate`
- `python manage.py runserver`
- `sudo systemctl restart gunicorn`

## A Causa

O último commit adicionou a biblioteca `bleach` ao `requirements.txt` para sanitização de dados nos formulários de registro. Essa biblioteca precisa ser instalada no seu ambiente Python.

## A Solução ✅

### Para Ambiente Local (Desenvolvimento)

1. **Ative seu ambiente virtual** (se você usa um):
   ```bash
   # Linux/Mac
   source .venv/bin/activate
   
   # Windows
   .venv\Scripts\activate
   ```

2. **Instale as dependências atualizadas:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Verifique se funcionou:**
   ```bash
   python -c "import bleach; print('✓ Sucesso! bleach está instalado')"
   ```

4. **Agora você pode executar os comandos Django:**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   python manage.py runserver
   ```

### Para Servidor de Produção (Azure/Linux)

1. **Conecte-se ao servidor via SSH**

2. **Navegue até o diretório do projeto:**
   ```bash
   cd ~/projeto_do_fim
   ```

3. **Ative o ambiente virtual:**
   ```bash
   source .venv/bin/activate
   ```

4. **Instale as dependências:**
   ```bash
   pip install -r requirements.txt
   ```

5. **Execute migrações (se necessário):**
   ```bash
   python manage.py migrate
   ```

6. **Reinicie os serviços:**
   ```bash
   sudo systemctl restart gunicorn nginx
   ```

7. **Verifique os logs:**
   ```bash
   sudo journalctl -u gunicorn -n 50 --no-pager
   ```

## Por Que Isso Aconteceu?

Quando você faz `git pull`, o Git atualiza os arquivos do código (incluindo `requirements.txt`), mas **NÃO instala automaticamente** as novas dependências Python. Você precisa executar manualmente `pip install -r requirements.txt` após cada `git pull` que adiciona novas bibliotecas.

## Como Evitar Isso No Futuro

**Sempre execute esses comandos após `git pull`:**

```bash
git pull origin main
pip install -r requirements.txt  # ← NÃO ESQUEÇA ESTE!
python manage.py migrate
python manage.py collectstatic --noinput
```

Você pode criar um alias ou script para facilitar:

```bash
# Adicione ao seu ~/.bashrc ou ~/.zshrc
alias update-projeto='git pull && pip install -r requirements.txt && python manage.py migrate && python manage.py collectstatic --noinput'
```

Depois, basta executar:
```bash
update-projeto
```

## O Que Foi Adicionado?

A biblioteca `bleach==6.2.0` foi adicionada para:
- ✅ Sanitizar campos de formulário (username, email, CPF)
- ✅ Remover tags HTML maliciosas
- ✅ Proteger contra ataques XSS (Cross-Site Scripting)
- ✅ Melhorar a segurança geral do sistema de registro

Para mais detalhes, veja [VALIDATION_CHANGES.md](VALIDATION_CHANGES.md).

## Precisa de Mais Ajuda?

Se você seguiu todos os passos e ainda tem problemas:

1. Verifique se você está no ambiente virtual correto
2. Verifique a versão do Python: `python --version` (deve ser 3.12+)
3. Tente instalar o bleach diretamente: `pip install bleach==6.2.0`
4. Veja [TROUBLESHOOTING.md](TROUBLESHOOTING.md) para mais soluções

---

**📚 Documentos Relacionados:**
- [VALIDATION_CHANGES.md](VALIDATION_CHANGES.md) - Mudanças no sistema de validação
- [TROUBLESHOOTING.md](TROUBLESHOOTING.md) - Guia completo de solução de problemas
- [SETUP_GUIDE.md](SETUP_GUIDE.md) - Guia de configuração do projeto
