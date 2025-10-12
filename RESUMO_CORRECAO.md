# 📝 Resumo da Correção - Erro do Módulo bleach

## 🎯 O Que Aconteceu?

Você fez `git pull` e recebeu este erro:
```
ModuleNotFoundError: No module named 'bleach'
```

### Por Que Aconteceu?

1. **No último commit**, foi adicionada a biblioteca `bleach` ao arquivo `requirements.txt`
2. Esta biblioteca é usada para **sanitizar dados** nos formulários de registro (limpar HTML malicioso)
3. O `git pull` baixou o código novo, mas **não instalou automaticamente** as novas dependências
4. Quando você tentou executar comandos Django, o Python não encontrou o módulo `bleach`

## ✅ A Solução (Rápida e Simples)

### No Seu Computador Local

```bash
# 1. Ative o ambiente virtual (se você usa um)
source .venv/bin/activate

# 2. Instale as dependências atualizadas
pip install -r requirements.txt

# 3. Pronto! Agora pode usar normalmente
python manage.py makemigrations
python manage.py migrate
python manage.py runserver
```

### No Servidor (Azure/Linux)

```bash
# 1. Conecte via SSH ao servidor
ssh azureuser@seu-servidor

# 2. Vá para o diretório do projeto
cd ~/projeto_do_fim

# 3. Ative o ambiente virtual
source .venv/bin/activate

# 4. Instale as dependências
pip install -r requirements.txt

# 5. Execute migrações (se necessário)
python manage.py makemigrations
python manage.py migrate

# 6. Reinicie os serviços
sudo systemctl restart gunicorn nginx
```

## 🔍 Por Que Não Aplicou no Localhost?

Você mencionou: *"No host local as modificações não foram aplicadas, o que pode ter acontecido?"*

**Resposta:** As modificações DO código foram aplicadas (você tem os arquivos atualizados), mas as **dependências Python** não foram instaladas automaticamente. 

O `git pull` atualiza apenas os arquivos do repositório, mas **NÃO instala** pacotes Python. Você precisa executar manualmente:

```bash
pip install -r requirements.txt
```

É como se você baixasse uma receita nova (o código), mas não comprasse os ingredientes (as bibliotecas Python) - você tem a receita, mas não consegue fazer o prato!

## 📚 O Que Foi Adicionado?

A biblioteca `bleach==6.2.0` foi adicionada para melhorar a segurança:

- ✅ Remove tags HTML maliciosas de inputs do usuário
- ✅ Protege contra ataques XSS (Cross-Site Scripting)
- ✅ Sanitiza username, email e CPF antes de salvar no banco
- ✅ Adiciona mais uma camada de proteção ao sistema

Veja mais detalhes em [VALIDATION_CHANGES.md](VALIDATION_CHANGES.md).

## 🛡️ Prevenção: Como Evitar Isso No Futuro

**Sempre que fizer `git pull`, execute em seguida:**

```bash
git pull origin main
pip install -r requirements.txt  # ← SEMPRE EXECUTE ISSO!
python manage.py migrate          # Se houver novas migrações
```

### Dica Pro: Crie um Alias

Adicione isso ao seu `~/.bashrc` ou `~/.zshrc`:

```bash
alias atualizar='git pull && pip install -r requirements.txt && python manage.py migrate && echo "✓ Projeto atualizado com sucesso!"'
```

Depois, sempre que precisar atualizar, basta digitar:
```bash
atualizar
```

## 📖 Documentação Atualizada

Foram criados/atualizados os seguintes documentos para ajudar:

1. **[FIX_BLEACH_ERROR.md](FIX_BLEACH_ERROR.md)** - Guia rápido em inglês
2. **[TROUBLESHOOTING.md](TROUBLESHOOTING.md)** - Adicionada seção sobre ModuleNotFoundError
3. **[VALIDATION_CHANGES.md](VALIDATION_CHANGES.md)** - Alerta sobre instalação do bleach
4. **[README.md](README.md)** - Adicionado erro comum e solução rápida
5. **[startup.sh](startup.sh)** - Script agora instala dependências automaticamente

## 🔧 Mudanças no startup.sh

O script `startup.sh` foi atualizado para instalar automaticamente as dependências quando o servidor inicia:

```bash
# ANTES
python manage.py migrate --noinput

# DEPOIS
pip install -r requirements.txt --quiet
python manage.py migrate --noinput
```

Isso significa que, **no servidor de produção**, as dependências serão instaladas automaticamente na próxima reinicialização.

## ✅ Checklist de Resolução

- [ ] Conectei ao servidor via SSH (se aplicável)
- [ ] Naveguei até o diretório do projeto: `cd ~/projeto_do_fim`
- [ ] Ativei o ambiente virtual: `source .venv/bin/activate`
- [ ] Instalei as dependências: `pip install -r requirements.txt`
- [ ] Verifiquei que funcionou: `python -c "import bleach; print('OK')"`
- [ ] Executei migrações: `python manage.py migrate`
- [ ] Reiniciei os serviços: `sudo systemctl restart gunicorn nginx`
- [ ] Testei o site: acessei as URLs para confirmar que está funcionando

## 🆘 Ainda Tendo Problemas?

Se você seguiu todos os passos e ainda está com erro:

1. **Verifique a versão do Python:**
   ```bash
   python --version
   ```
   Deve ser Python 3.12 ou superior.

2. **Verifique se está no ambiente virtual correto:**
   ```bash
   which python
   # Deve mostrar algo como: /home/azureuser/projeto_do_fim/.venv/bin/python
   ```

3. **Tente instalar o bleach diretamente:**
   ```bash
   pip install bleach==6.2.0
   ```

4. **Veja os logs do sistema:**
   ```bash
   # Logs do Gunicorn
   sudo journalctl -u gunicorn -n 100 --no-pager
   
   # Logs do Nginx
   sudo tail -n 100 /var/log/nginx/error.log
   ```

5. **Consulte a documentação completa:**
   - [FIX_BLEACH_ERROR.md](FIX_BLEACH_ERROR.md) - Guia detalhado
   - [TROUBLESHOOTING.md](TROUBLESHOOTING.md) - Problemas e soluções
   - [SETUP_GUIDE.md](SETUP_GUIDE.md) - Guia de configuração

## 📞 Suporte

Se nada disso resolver, abra uma issue no GitHub com:
- A saída do comando `pip list | grep bleach`
- A saída do comando `python --version`
- O erro completo que você está vendo
- O sistema operacional (Linux, Windows, Mac)

---

**Desenvolvido com ❤️ para o Portal de Análise**

*Última atualização: Outubro 2025*
