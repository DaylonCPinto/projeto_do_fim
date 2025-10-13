# Test Checklist - Header Fix (2025-10-13)

## ✅ Desktop Testing (PC)

### Home Page
- [ ] Acessar `/` (home page)
- [ ] Verificar se o "Destaque Principal" não está sendo coberto pelo header
- [ ] Verificar espaçamento adequado no topo (deve ter ~40px de margem)
- [ ] Scroll suave até o conteúdo funciona corretamente

### Section Pages
- [ ] Acessar `/geopolitica/`
  - [ ] Título "Geopolítica" totalmente visível (não coberto)
  - [ ] Espaçamento adequado entre header e título
  
- [ ] Acessar `/economia/`
  - [ ] Título "Economia" totalmente visível
  - [ ] Espaçamento adequado
  
- [ ] Acessar `/clima/`
  - [ ] Título "Clima" totalmente visível
  - [ ] Espaçamento adequado
  
- [ ] Acessar `/tecnologia/`
  - [ ] Título "Tecnologia" totalmente visível
  - [ ] Espaçamento adequado

### Different Resolutions (Desktop)
- [ ] 1920x1080 (Full HD)
  - [ ] Home page OK
  - [ ] Section pages OK
  
- [ ] 1366x768 (HD)
  - [ ] Home page OK
  - [ ] Section pages OK
  
- [ ] 1280x720 (HD Ready)
  - [ ] Home page OK
  - [ ] Section pages OK

## ✅ Mobile Testing (< 768px)

### Layout Verification
- [ ] Acessar home page em mobile
  - [ ] Layout não está com muito espaço em branco
  - [ ] Conteúdo visível sem scroll excessivo
  
- [ ] Acessar section pages em mobile
  - [ ] Títulos visíveis mas não com espaço excessivo
  - [ ] Layout continua otimizado

### Different Mobile Sizes
- [ ] 375x667 (iPhone SE)
- [ ] 414x896 (iPhone 11)
- [ ] 360x740 (Samsung Galaxy)

## ✅ Cross-Browser Testing

### Desktop Browsers
- [ ] Chrome/Edge (Chromium)
- [ ] Firefox
- [ ] Safari (se disponível)

### Mobile Browsers
- [ ] Chrome Mobile
- [ ] Safari Mobile (iOS)
- [ ] Samsung Internet

## ✅ Static Files

### Verificar se CSS está sendo servido corretamente
```bash
# No servidor, após deploy
python manage.py collectstatic --noinput
sudo systemctl restart gunicorn
sudo systemctl restart nginx
```

### Limpar cache do navegador
- [ ] Ctrl+Shift+R (Chrome/Firefox)
- [ ] Cmd+Shift+R (Safari)
- [ ] Verificar que a versão nova do CSS foi carregada

## 🔍 Debug Steps

Se o problema persistir:

1. **Verificar cache do navegador**
   - Abrir DevTools → Network
   - Verificar se custom.css está sendo carregado
   - Verificar timestamp do arquivo
   
2. **Verificar no servidor**
   ```bash
   # Ver se o arquivo foi atualizado
   ls -lah /path/to/static/css/custom.css
   
   # Ver conteúdo
   grep "padding-top: 4.6rem" /path/to/static/css/custom.css
   ```

3. **Forçar atualização**
   ```bash
   # Coletar arquivos estáticos novamente
   python manage.py collectstatic --clear --noinput
   
   # Reiniciar serviços
   sudo systemctl restart gunicorn nginx
   ```

4. **Verificar em modo anônimo**
   - Abrir janela anônima/privada
   - Testar novamente

## 📊 Valores Esperados (DevTools)

Inspecionar elemento `.section-header` no desktop deve mostrar:
```
padding-top: 4.6rem (calculado: ~73.6px)
margin-top: 2.3rem (calculado: ~36.8px)
```

Inspecionar elemento `.highlight-section:first-child` no desktop deve mostrar:
```
margin-top: 2.5rem (calculado: ~40px)
```

## ✅ Success Criteria

A correção é considerada bem-sucedida quando:

1. ✅ Títulos de seções não são cobertos pelo header no desktop
2. ✅ Destaque principal da home não é coberto no desktop
3. ✅ Layout mobile permanece otimizado (sem espaço excessivo)
4. ✅ Nenhuma quebra visual em qualquer resolução
5. ✅ Cross-browser compatibility mantida

---

**Última atualização:** 2025-10-13  
**Autor:** GitHub Copilot Agent  
**Issue:** Header covering content on PC
