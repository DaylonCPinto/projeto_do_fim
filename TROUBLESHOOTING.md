# Guia de Solução de Problemas - Portal de Análise

## 🔧 Problemas Resolvidos Neste PR

### 1. ✅ Header Cobrindo o Título das Seções

**Problema:** O header fixo cobria parte do título nas páginas de seção.

**Solução:** Adicionado padding-top de 2rem à classe `.section-header` no arquivo `static/css/custom.css`.

```css
.section-header {
    padding-top: 2rem;
    margin-top: 1rem;
}
```

### 2. ✅ Seção Geopolítica Não Criada

**Problema:** O comando `setup_site` não estava criando a seção de Geopolítica.

**Diagnóstico:**
Execute o comando de diagnóstico para verificar:
```bash
python manage.py check_sections
```

**Solução:**
Use o comando de correção dedicado:
```bash
python manage.py fix_geopolitica
```

Este comando irá:
- Verificar se já existe uma seção de Geopolítica
- Detectar conflitos de slug ou section_key
- Criar a seção se ela não existir
- Fornecer instruções claras se houver problemas

### 3. ✅ Melhor Tratamento de Erros no Setup

**Problema:** O comando `setup_site` não mostrava erros quando falhava ao criar seções.

**Solução:** Adicionado try/except com mensagens de erro claras no `setup_site.py`.

## 📋 Como Usar os Novos Comandos

### Verificar Estado das Seções

```bash
python manage.py check_sections
```

**Saída esperada:**
```
=== Checking Existing Sections ===

Found 5 SectionPages:

  - Title: "Geopolítica"
    Slug: geopolitica
    Section Key: geopolitica
    URL: /geopolitica/
    Live: True
    Articles: 3

  - Title: "Economia"
    Slug: economia
    Section Key: economia
    URL: /economia/
    Live: True
    Articles: 5

[... etc ...]

✅ All expected sections exist!
```

### Corrigir Seção Geopolítica

```bash
python manage.py fix_geopolitica
```

**Cenários:**

1. **Seção já existe:** Mostra a URL e confirma que está funcionando
2. **Conflito de slug:** Identifica páginas conflitantes e pede para removê-las
3. **Criação bem-sucedida:** Cria a seção e mostra a URL

## 🐛 Problemas Comuns e Soluções

### Problema: Seção existe mas não aparece

**Diagnóstico:**
```bash
python manage.py check_sections
```

**Possíveis causas:**
1. Página não está publicada (Live: False)
2. Slug incorreto
3. Section_key incorreto

**Solução:**
1. Acesse o admin do Wagtail em `/admin/pages/`
2. Encontre a página de seção
3. Verifique:
   - Status: deve estar "Publicado"
   - Slug: deve ser `geopolitica` (sem acento)
   - Section Key: deve ser `geopolitica`

### Problema: Imagens não aparecem nas seções

**Causa:** Templates de seção já estão corretos. Se as imagens não aparecem:

1. **Verifique se os artigos têm imagens:**
   - Artigos devem ter `external_image_url` OU `featured_image` preenchidos
   
2. **Para URLs externas:**
   - URL deve começar com `http://` ou `https://`
   - Servidor deve permitir acesso à imagem (CORS)
   
3. **Para imagens locais:**
   - Execute `python manage.py collectstatic`
   - Verifique configuração de MEDIA_URL e MEDIA_ROOT

### Problema: Erro 404 ao acessar /geopolitica/

**Causa:** Seção não existe ou não está publicada

**Solução:**
```bash
# 1. Diagnóstico
python manage.py check_sections

# 2. Se geopolítica está faltando:
python manage.py fix_geopolitica

# 3. Reinicie o servidor
sudo systemctl restart gunicorn nginx
```

## 🚀 Após as Correções

### Passo 1: Atualizar o código
```bash
git pull origin main
```

### Passo 2: Executar migrações (se houver)
```bash
python manage.py migrate
```

### Passo 3: Coletar arquivos estáticos
```bash
python manage.py collectstatic --noinput
```

### Passo 4: Verificar seções
```bash
python manage.py check_sections
```

### Passo 5: Corrigir geopolítica (se necessário)
```bash
python manage.py fix_geopolitica
```

### Passo 6: Reiniciar serviços
```bash
sudo systemctl restart gunicorn nginx
```

### Passo 7: Testar
Acesse as URLs:
- `/` - Home (deve mostrar Em Alta)
- `/geopolitica/` - Geopolítica
- `/economia/` - Economia
- `/clima/` - Clima
- `/tecnologia/` - Tecnologia
- `/escatologia/` - Escatologia

## 📸 Mudanças Visuais

### Header com Espaçamento Correto
O título das seções agora tem espaçamento adequado e não é coberto pelo header fixo.

**Antes:** Título cortado pelo header
**Depois:** Título visível com espaçamento de 2rem

## 🔍 Debug Adicional

Se ainda houver problemas, execute:

```bash
# Ver logs do Gunicorn
sudo journalctl -u gunicorn -n 50 --no-pager

# Ver logs do Nginx
sudo tail -n 50 /var/log/nginx/error.log

# Testar no shell do Django
python manage.py shell
>>> from content.models import SectionPage
>>> SectionPage.objects.all()
>>> SectionPage.objects.filter(section_key='geopolitica')
```

## 📞 Precisa de Mais Ajuda?

Se os comandos acima não resolverem:

1. Execute `python manage.py check_sections` e compartilhe a saída
2. Execute `python manage.py fix_geopolitica` e compartilhe qualquer erro
3. Verifique os logs: `sudo journalctl -u gunicorn -n 100`
