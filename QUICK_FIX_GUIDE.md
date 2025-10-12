# 🚀 Guia Rápido de Correção

## ⚡ Aplicação Rápida (5 minutos)

### 1️⃣ Atualizar código
```bash
cd ~/projeto_do_fim
git pull origin main
```

### 2️⃣ Coletar arquivos estáticos (para CSS)
```bash
python manage.py collectstatic --noinput
```

### 3️⃣ Verificar seções
```bash
python manage.py check_sections
```

### 4️⃣ Corrigir Geopolítica (se necessário)
```bash
python manage.py fix_geopolitica
```

### 5️⃣ Reiniciar
```bash
sudo systemctl restart gunicorn nginx
```

### 6️⃣ Testar
Abra no navegador:
- `/geopolitica/` ✅
- `/economia/` ✅
- `/clima/` ✅
- `/tecnologia/` ✅
- `/escatologia/` ✅

---

## 🎯 O Que Foi Corrigido?

### ✅ Problema 1: Header Cobria o Título
**Antes:** Título ficava parcialmente escondido atrás do header fixo  
**Depois:** Título visível com espaçamento adequado  
**Arquivo:** `static/css/custom.css`

### ✅ Problema 2: Geopolítica Não Criada
**Antes:** Setup falhava silenciosamente  
**Depois:** Comando dedicado `fix_geopolitica` para corrigir  
**Arquivos:** Novos comandos de gestão

### ✅ Problema 3: Imagens (Já Funcionava)
**Status:** Templates corretos, imagens devem funcionar  
**Se não funcionar:** Verificar que artigos têm imagens configuradas

---

## 🔍 Comandos de Diagnóstico

### Ver todas as seções
```bash
python manage.py check_sections
```

### Corrigir Geopolítica especificamente
```bash
python manage.py fix_geopolitica
```

### Ver logs se houver erro
```bash
sudo journalctl -u gunicorn -n 50 --no-pager
```

---

## 📊 Saída Esperada

### Sucesso: `check_sections`
```
✅ All expected sections exist!
```

### Sucesso: `fix_geopolitica`
```
✅ Created Geopolítica section successfully!
   URL: /geopolitica/
```

---

## ⚠️ Problemas Comuns

### "Seção já existe mas não aparece"
**Solução:**
1. Verifique que está publicada no admin
2. Verifique o slug (deve ser `geopolitica` sem acento)

### "Erro ao criar seção"
**Solução:**
1. Execute `check_sections` para ver conflitos
2. Delete páginas conflitantes no admin
3. Execute `fix_geopolitica` novamente

### "Imagens não aparecem"
**Solução:**
1. Verifique que artigos têm imagens (external_image_url ou featured_image)
2. Execute `collectstatic` novamente
3. Verifique URLs de imagens externas

---

## 📚 Documentação Completa

Para detalhes técnicos, veja:
- `TROUBLESHOOTING.md` - Guia completo de solução de problemas
- `CHANGES_SUMMARY.md` - Resumo técnico das mudanças
- `VISUAL_CHANGES.md` - Documentação visual antes/depois

---

## 💡 Dica Pro

Após qualquer mudança, sempre:
```bash
# 1. Coletar estáticos
python manage.py collectstatic --noinput

# 2. Verificar
python manage.py check_sections

# 3. Reiniciar
sudo systemctl restart gunicorn nginx
```

---

## ✅ Checklist Final

Marque conforme completa:

- [ ] Código atualizado (`git pull`)
- [ ] Estáticos coletados (`collectstatic`)
- [ ] Seções verificadas (`check_sections`)
- [ ] Geopolítica corrigida se necessário (`fix_geopolitica`)
- [ ] Serviços reiniciados (`systemctl restart`)
- [ ] URLs testadas no navegador
- [ ] Títulos não cobertos pelo header ✓
- [ ] Todas as seções acessíveis ✓

---

## 🎉 Pronto!

Seu site deve estar funcionando perfeitamente com:
- ✅ Títulos visíveis em todas as seções
- ✅ Geopolítica criada e funcionando
- ✅ Todas as 5 seções acessíveis
- ✅ Imagens carregando corretamente

**Se ainda houver problemas:** Execute `check_sections` e compartilhe a saída.
