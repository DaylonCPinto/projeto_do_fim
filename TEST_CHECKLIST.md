# Checklist de Testes - Portal Modernizado

## ✅ Testes Funcionais

### 🏠 Página Inicial (Home)

#### Layout e Estrutura
- [ ] Header aparece fixo no topo
- [ ] Barra superior mostra data atual
- [ ] Logo e nome do site visíveis
- [ ] Menu de navegação funciona
- [ ] Pills de categorias visíveis (desktop)
- [ ] Artigo em destaque carrega corretamente
- [ ] Seção de vídeos aparece (se configurada)
- [ ] Grid de artigos exibe corretamente
- [ ] Footer aparece completo

#### Funcionalidade
- [ ] Scroll suave funciona
- [ ] Barra de progresso de scroll aparece
- [ ] Hover effects nos cards funcionam
- [ ] Links redirecionam corretamente
- [ ] Botões de login/logout funcionam
- [ ] Status de assinatura aparece (se logado)

### 📹 Seção de Vídeos

#### Exibição
- [ ] Vídeos destacados aparecem
- [ ] Thumbnails carregam corretamente
- [ ] Play overlay visível
- [ ] Título e duração aparecem
- [ ] Hover effect funciona
- [ ] Grid responsivo (4 col desktop, 2 mobile)

#### Funcionalidade
- [ ] Click no card abre vídeo
- [ ] URLs dos vídeos estão corretas
- [ ] "Ver todos" funciona (ou desabilitado)

### 🎨 Customização do Site

#### Admin Django
- [ ] Acesso ao Site Customization funciona
- [ ] Campos de fonte editáveis
- [ ] Campos de cor funcionam (color picker)
- [ ] Checkbox de vídeos funciona
- [ ] Input de artigos por página funciona
- [ ] Salvar aplica mudanças

#### Frontend
- [ ] Mudanças de fonte refletem no site
- [ ] Mudanças de cor aplicadas
- [ ] Vídeos aparecem/desaparecem conforme config
- [ ] Número de artigos respeita configuração

### 👤 Sistema de Usuários

#### Autenticação
- [ ] Login funciona
- [ ] Logout funciona
- [ ] Cadastro funciona
- [ ] Informações do usuário aparecem no header
- [ ] Status premium/gratuito correto

#### Permissões
- [ ] Usuários não-autenticados veem botão "Assinar"
- [ ] Usuários autenticados veem status de assinatura
- [ ] Conteúdo premium bloqueado adequadamente

### 📝 Gerenciamento de Conteúdo

#### Artigos no Wagtail
- [ ] Criar novo artigo funciona
- [ ] Editar artigo existente funciona
- [ ] Upload de imagem local funciona
- [ ] URL de imagem externa funciona
- [ ] Prioridade de imagem externa correta
- [ ] Tags funcionam
- [ ] Publicação funciona
- [ ] Artigo aparece na home após publicar

#### Vídeos no Django Admin
- [ ] Adicionar vídeo funciona
- [ ] Editar vídeo funciona
- [ ] Marcar como destaque funciona
- [ ] Preview do thumbnail aparece
- [ ] Badge de status aparece
- [ ] Ordem de exibição funciona
- [ ] Deletar vídeo funciona

### 🕐 Timezone e Datas

#### Exibição de Datas
- [ ] Data de publicação em formato correto
- [ ] "Publicado há X tempo" em português
- [ ] Tempo calculado no timezone de Brasília
- [ ] Data atual no header correta

### 💅 Estilos e CSS

#### Header
- [ ] Cores corretas
- [ ] Sombra aparece
- [ ] Hover effects funcionam
- [ ] Dropdown de seções funciona
- [ ] Responsivo no mobile

#### Footer
- [ ] Newsletter seção visível
- [ ] Links organizados corretamente
- [ ] Ícones sociais aparecem
- [ ] Hover effects funcionam
- [ ] Copyright e info corretos

#### Cards e Elementos
- [ ] Article cards com sombra
- [ ] Hover eleva o card
- [ ] Premium badge aparece
- [ ] Highlight section destaca
- [ ] Video cards responsivos

### 🎭 Admin Customizado

#### Wagtail Admin
- [ ] CSS customizado carrega
- [ ] Cores da marca aplicadas
- [ ] Botões estilizados
- [ ] Sidebar com cores corretas
- [ ] Painéis com borda vermelha

#### Django Admin
- [ ] VideoShortAdmin formatado
- [ ] SiteCustomizationAdmin formatado
- [ ] UserProfileAdmin formatado
- [ ] Badges coloridos funcionam
- [ ] Ações em massa funcionam

### 📱 Responsividade

#### Mobile (< 768px)
- [ ] Header colapsa corretamente
- [ ] Menu hambúrguer funciona
- [ ] Pills de categoria ocultos
- [ ] Footer reorganizado
- [ ] Vídeos em 2 colunas
- [ ] Artigos em 1 coluna
- [ ] Texto legível
- [ ] Botões acessíveis

#### Tablet (768px - 1024px)
- [ ] Layout intermediário correto
- [ ] Navegação funciona
- [ ] Grid de artigos adequado
- [ ] Vídeos visíveis
- [ ] Footer organizado

#### Desktop (> 1024px)
- [ ] Layout completo
- [ ] Pills de categoria visíveis
- [ ] Grid de 3 colunas para artigos
- [ ] 4 colunas para vídeos
- [ ] Footer em linha

### 🚀 JavaScript

#### Funcionalidades
- [ ] main.js carrega sem erros
- [ ] Scroll progress bar funciona
- [ ] Smooth scroll funciona
- [ ] Tempo de leitura aparece
- [ ] Newsletter validation funciona
- [ ] Toast notifications aparecem
- [ ] Share button funciona
- [ ] Lazy loading ativo

#### Console
- [ ] Sem erros no console
- [ ] Mensagem de boas-vindas aparece
- [ ] Logs apropriados

### 🔐 Segurança

#### Configurações
- [ ] DEBUG=False em produção
- [ ] SECRET_KEY não exposta
- [ ] ALLOWED_HOSTS configurado
- [ ] CSRF_TRUSTED_ORIGINS correto
- [ ] SSL redirect ativo (produção)

#### Proteção
- [ ] CSRF tokens presentes
- [ ] XSS protection ativa
- [ ] Clickjacking protection ativa
- [ ] Content type sniffing bloqueado

### ⚡ Performance

#### Carregamento
- [ ] Página carrega < 3s
- [ ] First Contentful Paint < 1.5s
- [ ] CSS minificado em produção
- [ ] JS minificado em produção
- [ ] Imagens otimizadas

#### Otimizações
- [ ] Static files coletados
- [ ] Whitenoise configurado
- [ ] Gzip habilitado
- [ ] Cache-Control headers
- [ ] Lazy loading ativo

### 🐛 Bugs Conhecidos

#### Verificar e Corrigir
- [ ] Verificar erros de console
- [ ] Testar em diferentes navegadores
- [ ] Testar em diferentes dispositivos
- [ ] Verificar links quebrados
- [ ] Validar HTML/CSS
- [ ] Verificar acessibilidade

### 📊 Compatibilidade de Navegadores

#### Desktop
- [ ] Chrome/Edge (últimas 2 versões)
- [ ] Firefox (últimas 2 versões)
- [ ] Safari (última versão)

#### Mobile
- [ ] Chrome Mobile
- [ ] Safari iOS
- [ ] Samsung Internet

---

## 🎯 Resultado dos Testes

### Funcionalidades Principais
- **Header**: ✅ / ⚠️ / ❌
- **Footer**: ✅ / ⚠️ / ❌
- **Vídeos**: ✅ / ⚠️ / ❌
- **Customização**: ✅ / ⚠️ / ❌
- **Timezone**: ✅ / ⚠️ / ❌
- **JavaScript**: ✅ / ⚠️ / ❌
- **Admin**: ✅ / ⚠️ / ❌
- **Responsividade**: ✅ / ⚠️ / ❌

### Notas
```
Adicione aqui quaisquer observações ou bugs encontrados:

1. 
2. 
3. 
```

### Status Geral
- [ ] Todos os testes passaram
- [ ] Pequenos ajustes necessários
- [ ] Correções importantes necessárias

---

**Data do Teste**: _______________  
**Testado por**: _______________  
**Ambiente**: Desenvolvimento / Staging / Produção
