# Guia Rápido de Configuração - Portal Modernizado

## 🚀 Início Rápido

### 1. Preparar Ambiente
```bash
# Instalar dependências
pip install -r requirements.txt

# Executar migrações
python manage.py migrate

# Coletar arquivos estáticos
python manage.py collectstatic --noinput

# Criar superusuário (se ainda não existe)
python manage.py createsuperuser
```

### 2. Configurar Customização do Site
```bash
# Acessar o admin Django
# URL: http://seudominio.com/django-admin/

# Navegar para: Content > Site customizations
# Clicar em "Add Site Customization"
```

**Configure:**
- **Heading Font**: Roboto, Montserrat, Playfair Display, etc.
- **Body Font**: Merriweather, Open Sans, Lora, etc.
- **Primary Color**: #E3120B (ou sua cor preferida)
- **Secondary Color**: #111111 (ou sua cor preferida)
- **Show Video Section**: ✓ (ativar seção de vídeos)
- **Articles Per Page**: 9 (ou quantos preferir)

### 3. Adicionar Vídeos em Destaque
```bash
# Acessar: /django-admin/content/videoshort/
# Clicar em "Add Video Short"
```

**Preencher:**
- **Título**: Ex: "Análise da Economia"
- **Descrição**: Breve descrição do vídeo
- **URL do Vídeo**: Link do YouTube, Vimeo, etc.
- **Thumbnail**: Upload de imagem OU URL externa
- **Duração**: Ex: "1:30"
- **Destacar na Home?**: ✓ (para aparecer na home)
- **Ordem**: 0, 1, 2, 3... (ordem de exibição)

### 4. Usar Imagens Externas em Artigos

**Economizar espaço usando URLs:**
```bash
# No Wagtail Admin (/admin/)
# Editar ou criar um artigo
# Seção "Imagem de Destaque"
```

**Opção 1 - URL Externa** (recomendado para economizar espaço):
- Cole a URL completa da imagem
- Ex: https://example.com/images/noticia.jpg

**Opção 2 - Upload Local**:
- Faça upload da imagem
- Ideal para imagens permanentes

**Nota**: Se ambos estiverem preenchidos, a URL externa terá prioridade.

---

## 🎨 Personalização Visual

### Alterar Cores Principais
1. Admin Django → Site Customization
2. Modificar "Primary Color" e "Secondary Color"
3. Usar formato hexadecimal: #RRGGBB
4. Salvar

### Mudar Fontes
1. Escolha fontes do Google Fonts
2. Exemplos populares:
   - **Títulos**: Roboto, Montserrat, Poppins, Raleway
   - **Corpo**: Merriweather, Lora, Open Sans, Source Sans Pro
3. Digite apenas o nome da fonte (sem espaços extras)

---

## 📹 Gerenciar Vídeos

### Adicionar Novo Vídeo
```
/django-admin/content/videoshort/add/
```

### Editar Vídeos Existentes
```
/django-admin/content/videoshort/
```

### Marcar Vídeos como Destaque em Massa
1. Selecionar vídeos desejados
2. Em "Action", escolher "★ Marcar como destaque"
3. Clicar em "Go"

### Dicas:
- Mantenha até 4 vídeos destacados para melhor visualização
- Use thumbnails com proporção 9:16 (vertical) para melhor resultado
- Duração ideal: 30s a 2min

---

## 🔧 Solução de Problemas Comuns

### CSS não está carregando
```bash
python manage.py collectstatic --clear --noinput
```

### Vídeos não aparecem
1. Verificar se "is_featured" está marcado
2. Verificar se existe pelo menos 1 vídeo
3. Limpar cache do navegador (Ctrl+F5)

### Timezone incorreto
- Verificar em settings.py: `TIME_ZONE = 'America/Sao_Paulo'`
- O filtro `timesince_brasilia` foi implementado automaticamente

### Erro 500 em produção
1. Verificar `DEBUG=False` no .env
2. Executar `python manage.py check --deploy`
3. Verificar logs: `python manage.py check`

---

## 📱 Recursos Implementados

### Frontend
✅ Header com 3 níveis de navegação  
✅ Footer com newsletter e links sociais  
✅ Seção de vídeos curtos  
✅ Sistema de highlights  
✅ Barra de progresso de scroll  
✅ Tempo de leitura estimado  
✅ Toast notifications  
✅ Smooth scrolling  
✅ Lazy loading de imagens  

### Backend
✅ Modelo VideoShort  
✅ Modelo SiteCustomization  
✅ Suporte a imagens externas (URL)  
✅ Admin customizado  
✅ Filtro timezone Brasília  
✅ Wagtail hooks personalizados  

---

## 🎯 URLs Importantes

### Frontend (Público)
- **Home**: `/`
- **Login**: `/accounts/login/`
- **Cadastro**: `/accounts/signup/`

### Admin (Restrito)
- **Wagtail Admin**: `/admin/`
- **Django Admin**: `/django-admin/`
- **Vídeos**: `/django-admin/content/videoshort/`
- **Customização**: `/django-admin/content/sitecustomization/`
- **Artigos**: `/admin/pages/`
- **Imagens**: `/admin/images/`

---

## 📊 Checklist de Deploy

Antes de fazer deploy em produção:

- [ ] Executar `python manage.py check --deploy`
- [ ] Configurar variáveis de ambiente no .env
- [ ] Definir `DEBUG=False`
- [ ] Configurar `ALLOWED_HOSTS`
- [ ] Configurar `CSRF_TRUSTED_ORIGINS`
- [ ] Executar migrações: `python manage.py migrate`
- [ ] Coletar estáticos: `python manage.py collectstatic`
- [ ] Criar customização do site
- [ ] Adicionar vídeos em destaque
- [ ] Testar em diferentes dispositivos
- [ ] Verificar performance com Lighthouse

---

## 🌟 Boas Práticas

### Imagens
- Use URLs externas para economizar espaço
- Otimize imagens antes do upload (WebP, PNG, JPG)
- Dimensões recomendadas: 1200x630px para featured images

### Vídeos
- Hospede vídeos no YouTube/Vimeo
- Use thumbnails atrativos
- Mantenha vídeos curtos (< 2min)

### Conteúdo
- Escreva títulos concisos (< 60 caracteres)
- Introduções com 150-250 caracteres
- Use tags para categorização
- Marque conteúdo premium apropriadamente

### Performance
- Ative cache em produção
- Use CDN para assets estáticos
- Monitore performance com ferramentas
- Otimize banco de dados regularmente

---

## 📞 Suporte

Para mais informações, consulte:
- **MODERNIZATION_GUIDE.md**: Documentação completa
- **README.md**: Informações gerais do projeto
- **FEATURES_GUIDE.md**: Guia de funcionalidades

---

**Desenvolvido com ❤️ por Daylon C. Pinto**  
**Versão**: 2.0 - Modernização Completa
