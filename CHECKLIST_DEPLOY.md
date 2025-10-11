# ✅ Checklist de Deploy - Azure VMs

**Imprima esta página e marque conforme avança!**

---

## 📋 FASE 1: PREPARAÇÃO (5 min)

### Informações que você precisa ter em mãos:

- [ ] IP Público da VM Web: `_____________________`
- [ ] IP Privado da VM Database: `_____________________`
- [ ] Usuário SSH: `_____________________`
- [ ] Resource Group VM Web: `_____________________`
- [ ] Resource Group VM Database: `_____________________`
- [ ] Nome NSG VM Web: `_____________________`
- [ ] Nome NSG VM Database: `_____________________`

### Testes iniciais:

- [ ] Consigo fazer SSH na VM Web: `ssh azureuser@IP_WEB`
- [ ] Azure CLI instalado no meu computador: `az --version`
- [ ] Logado no Azure CLI: `az account show`

---

## 🌐 FASE 2: CONFIGURAÇÃO DE REDE (10 min)

### VNet Peering (se VMs em VNets diferentes):

- [ ] Verificado se VMs estão na mesma VNet
- [ ] Se diferentes: Peering criado Web → DB
- [ ] Se diferentes: Peering criado DB → Web
- [ ] Peerings em status "Connected"

### NSG da VM Web:

- [ ] Porta 22 (SSH) aberta
- [ ] Porta 80 (HTTP) aberta
- [ ] Porta 443 (HTTPS) aberta

**Comando usado**:
```bash
./scripts/configure_azure_nsg.sh
```
**Executado em**: ____________ às ______

### NSG da VM Database:

- [ ] Porta 5432 (PostgreSQL) aberta APENAS para IP da VM Web
- [ ] IP da VM Web configurado na regra: `_____________________`

---

## 🗄️ FASE 3: CONFIGURAÇÃO DATABASE (15 min)

### Conexão SSH:

- [ ] SSH jump configurado no ~/.ssh/config
- [ ] Consegui conectar na VM DB: `ssh azure-db`

### Script de Setup:

- [ ] Script baixado: `wget https://...setup_database.sh`
- [ ] Permissão de execução dada: `chmod +x setup_database.sh`
- [ ] Script executado: `sudo ./setup_database.sh`

### Credenciais anotadas:

```
Banco de dados: ___________________________
Usuário: ___________________________
Senha: ___________________________
Host (IP privado): ___________________________
Porta: 5432
```

### Verificações:

- [ ] PostgreSQL rodando: `sudo systemctl status postgresql`
- [ ] Porta 5432 aberta: `sudo netstat -plnt | grep 5432`
- [ ] Firewall configurado: `sudo ufw status`

---

## 🌐 FASE 4: CONFIGURAÇÃO WEB (20 min)

### Conexão SSH:

- [ ] Conectado na VM Web: `ssh azureuser@IP_PUBLICO`

### Script de Setup:

- [ ] Script baixado: `wget https://...setup_web.sh`
- [ ] Permissão de execução dada: `chmod +x setup_web.sh`
- [ ] Script executado: `sudo ./setup_web.sh`

### Configuração do .env:

- [ ] Mudei para usuário django: `sudo su - django`
- [ ] Copiei template: `cp .env.template .env`
- [ ] Gerei SECRET_KEY nova
- [ ] Editei .env com credenciais corretas
- [ ] DATABASE_URL configurada corretamente

**DATABASE_URL configurada**:
```
postgres://USUARIO:SENHA@IP_DB:5432/BANCO
```

### Preparação Django:

- [ ] Ambiente virtual ativado: `source venv/bin/activate`
- [ ] Migrações executadas: `python manage.py migrate`
- [ ] Static files coletados: `python manage.py collectstatic --noinput`
- [ ] Superusuário criado: `python manage.py createsuperuser`

**Credenciais do superusuário**:
```
Username: ___________________________
Email: ___________________________
Senha: ___________________________
```

### Iniciar Serviços:

- [ ] Voltei para usuário root: `exit`
- [ ] Supervisor recarregado: `sudo supervisorctl reread`
- [ ] Supervisor atualizado: `sudo supervisorctl update`
- [ ] Gunicorn iniciado: `sudo supervisorctl start django`
- [ ] Status verificado: `sudo supervisorctl status django`
- [ ] Nginx reiniciado: `sudo systemctl restart nginx`
- [ ] Status verificado: `sudo systemctl status nginx`

---

## 🔍 FASE 5: TESTES E VERIFICAÇÃO (5 min)

### Teste de Conectividade:

- [ ] Script de teste baixado: `wget https://...test_connectivity.sh`
- [ ] Script executado: `./test_connectivity.sh`
- [ ] Todos os testes passaram ✓

### Verificação de Logs:

- [ ] Gunicorn sem erros: `sudo tail -100 /var/log/django/gunicorn.log`
- [ ] Nginx sem erros: `sudo tail -100 /var/log/nginx/django_error.log`

### Testes no Navegador:

- [ ] Site abre: `http://IP_PUBLICO`
- [ ] CSS carrega corretamente
- [ ] JavaScript funciona
- [ ] Admin acessível: `http://IP_PUBLICO/admin/`
- [ ] Wagtail CMS acessível: `http://IP_PUBLICO/cms/`
- [ ] Login funciona no admin
- [ ] Upload de imagens funciona

---

## ✅ VERIFICAÇÃO FINAL

### Serviços Rodando:

- [ ] PostgreSQL rodando na VM DB
- [ ] Gunicorn rodando na VM Web
- [ ] Nginx rodando na VM Web
- [ ] Todos os serviços configurados para auto-start

### Segurança:

- [ ] DEBUG=False no .env
- [ ] SECRET_KEY forte e única
- [ ] Senha do banco de dados forte
- [ ] Credenciais anotadas em local seguro
- [ ] NSG configurado corretamente

### Funcionalidade:

- [ ] Site completamente funcional
- [ ] Sem erros 502 Bad Gateway
- [ ] Sem erros de conexão com banco
- [ ] Static files carregam
- [ ] Upload de arquivos funciona
- [ ] Admin e CMS funcionam

---

## 📝 ANOTAÇÕES E PROBLEMAS

Use este espaço para anotar qualquer problema ou observação:

```
____________________________________________________________________

____________________________________________________________________

____________________________________________________________________

____________________________________________________________________

____________________________________________________________________

____________________________________________________________________

____________________________________________________________________

____________________________________________________________________
```

---

## 🔄 PRÓXIMOS PASSOS (OPCIONAL)

### SSL/HTTPS (se tem domínio):

- [ ] Domínio configurado apontando para IP público
- [ ] Certbot instalado
- [ ] Certificado SSL obtido
- [ ] .env atualizado com domínio
- [ ] Renovação automática testada

### Backup:

- [ ] Script de backup do banco configurado
- [ ] Cron job de backup configurado
- [ ] Testado restore de backup

### Monitoramento:

- [ ] Azure Monitor configurado
- [ ] Alertas configurados
- [ ] Dashboard criado

---

## ⏱️ TEMPO TOTAL

**Início**: _______ às _______

**Fim**: _______ às _______

**Tempo total**: _______ minutos

**Tempo estimado**: 55 minutos

---

## 📞 SUPORTE

Se teve problemas, consulte:

1. **[TROUBLESHOOTING_NGINX_GUNICORN.md](TROUBLESHOOTING_NGINX_GUNICORN.md)**
2. **[AZURE_VM_SETUP_COMPLETO.md](AZURE_VM_SETUP_COMPLETO.md)**
3. Logs: `/var/log/django/gunicorn.log` e `/var/log/nginx/django_error.log`

---

## ✨ DEPLOY COMPLETO!

**Parabéns! Seu site está no ar! 🎉**

URL do site: `http://_______________________`

Data do deploy: _______________

---

**Para atualizações futuras, consulte**: [GUIA_RAPIDO_AZURE.md - Seção Deploy](GUIA_RAPIDO_AZURE.md#🔄-atualizar-código-deploy)
