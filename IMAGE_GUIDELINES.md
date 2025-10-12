# Guia de Tamanhos de Imagens

Este documento fornece orientações sobre os tamanhos recomendados de imagens para diferentes seções do site.

## 📏 Tamanhos Recomendados

### Imagens de Artigos

#### 1. Imagem de Destaque (Featured Image)
- **Tamanho Recomendado**: 1200x630 pixels (proporção 1.91:1)
- **Tamanho Mínimo**: 800x420 pixels
- **Formato**: JPG ou PNG
- **Peso Máximo**: 500KB (otimizado para web)
- **Uso**: Aparece no topo dos artigos e nos cards de preview

#### 2. Imagens dentro do Conteúdo do Artigo
- **Tamanho Recomendado**: 1000x750 pixels (proporção 4:3)
- **Tamanho Alternativo**: 1000x562 pixels (proporção 16:9)
- **Formato**: JPG ou PNG
- **Peso Máximo**: 400KB
- **Uso**: Imagens incorporadas no corpo do artigo

#### 3. GIFs Animados
- **Tamanho Recomendado**: 800x600 pixels ou menor
- **Formato**: GIF
- **Peso Máximo**: 2MB (GIFs maiores podem causar lentidão)
- **Uso**: Ilustrações animadas dentro dos artigos

### Imagens de Vídeos Curtos

#### 4. Thumbnails de Vídeos (Shorts)
- **Tamanho Recomendado**: 400x700 pixels (proporção 9:16 - vertical)
- **Tamanho Alternativo**: 400x600 pixels
- **Formato**: JPG ou PNG
- **Peso Máximo**: 300KB
- **Uso**: Miniaturas dos vídeos curtos na página de vídeos e home

### Imagens de Páginas

#### 5. Banners/Headers de Seção
- **Tamanho Recomendado**: 1920x400 pixels (proporção 4.8:1)
- **Formato**: JPG ou PNG
- **Peso Máximo**: 600KB
- **Uso**: Cabeçalhos de páginas de seção

## 🎨 Diretrizes de Qualidade

### Resolução e Densidade de Pixels
- Use imagens com pelo menos 72 DPI para web
- Para displays retina/HD, considere imagens 2x maiores (mas otimize o peso)

### Otimização
- **Sempre otimize suas imagens antes do upload**
- Ferramentas recomendadas:
  - [TinyPNG](https://tinypng.com/) - Compressão PNG/JPG
  - [Squoosh](https://squoosh.app/) - Compressão universal
  - [GIFSICLE](https://www.lcdf.org/gifsicle/) - Otimização de GIFs

### Formato
- **JPG**: Use para fotos e imagens com muitas cores
- **PNG**: Use para gráficos, logos, e imagens com transparência
- **GIF**: Use apenas para animações curtas
- **WebP**: Formato moderno (recomendado se suportado)

## 📱 Responsividade

Todas as imagens são automaticamente ajustadas para diferentes tamanhos de tela:
- **Desktop**: Tamanho completo
- **Tablet**: Redimensionado proporcionalmente
- **Mobile**: Redimensionado para 100% da largura da tela

## 🔧 Upload de Imagens

### Opção 1: Upload Direto (Recomendado para Digital Ocean Spaces)
1. Faça upload da imagem para o Digital Ocean Spaces
2. Copie a URL pública da imagem
3. Cole a URL no campo "URL de Imagem Externa" no admin

### Opção 2: Upload Local (Banco de Dados)
1. Use o campo "Imagem de Destaque" ou "Imagem (Upload)"
2. Selecione a imagem do seu computador
3. O Wagtail armazenará a imagem no servidor

## 📊 Referência Rápida

| Tipo de Imagem | Tamanho (px) | Proporção | Peso Max |
|----------------|--------------|-----------|----------|
| Featured (Destaque) | 1200x630 | 1.91:1 | 500KB |
| Conteúdo Artigo | 1000x750 | 4:3 | 400KB |
| GIF Animado | 800x600 | 4:3 | 2MB |
| Thumbnail Vídeo | 400x700 | 9:16 | 300KB |
| Banner Seção | 1920x400 | 4.8:1 | 600KB |

## 💡 Dicas Importantes

1. **Sem Imagens Automáticas**: O sistema não adiciona mais imagens de placeholder automaticamente. Certifique-se de adicionar imagens reais aos seus artigos.

2. **Consistência Visual**: Mantenha um estilo visual consistente em todas as imagens do site.

3. **Direitos Autorais**: Use apenas imagens que você tem direito de usar (próprias, licenças, ou domínio público).

4. **Acessibilidade**: Sempre adicione textos alternativos (alt text) descritivos para suas imagens.

5. **Performance**: Imagens otimizadas melhoram significativamente o tempo de carregamento do site.

## 🎯 Testando Imagens

Antes de publicar um artigo:
1. Visualize em diferentes tamanhos de tela
2. Verifique se as imagens carregam corretamente
3. Confirme que o peso total da página está adequado
4. Teste a velocidade de carregamento

---

**Nota**: Estas são recomendações. O sistema aceita outros tamanhos, mas seguir estas diretrizes garante a melhor apresentação visual e performance.
