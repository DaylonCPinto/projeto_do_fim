# FonteLinkBlock - Documentação

## Descrição

O **FonteLinkBlock** (Fonte com Link) é um bloco personalizado do Wagtail que permite aos editores adicionar citações de fontes com links estilizados de forma elegante e consistente.

## Funcionalidade

Este bloco exibe o texto "Fonte:" seguido de um link estilizado que:
- Aparece em vermelho (#E3120B - cor primária do site)
- É clicável e abre em uma nova aba
- Não exibe a URL completa, apenas o texto da fonte (ex: "CNN", "Reuters", "BBC")
- Tem peso de fonte 500 (semi-bold)
- Não tem sublinhado por padrão

## Como Usar no Admin

1. Ao editar um artigo, role até a seção "Conteúdo do Artigo"
2. Clique em "Adicionar bloco" (+ icon)
3. Selecione "Fonte com Link" da lista de blocos disponíveis
4. Preencha os dois campos:
   - **Texto da Fonte**: O nome da fonte que aparecerá clicável (ex: "CNN", "Reuters", "G1")
   - **URL da Fonte**: O link completo para a fonte (ex: https://www.cnnbrasil.com.br/internacional/...)

## Exemplo de Uso

### Entrada no Admin:
- **Texto da Fonte**: CNN
- **URL da Fonte**: https://www.cnnbrasil.com.br/internacional/hamas-lista-refens-vivos/

### Saída Renderizada:
```
Fonte: CNN (em vermelho, clicável)
```

## Estrutura Técnica

### Localização dos Arquivos

- **Modelo**: `/content/models.py` - Classe `FonteLinkBlock`
- **Template**: `/content/templates/content/blocks/fonte_link_block.html`
- **Migration**: `/content/migrations/0019_alter_articlepage_content_blocks.py`

### Código do Modelo

```python
class FonteLinkBlock(blocks.StructBlock):
    """Block for displaying a source link with custom styled text"""
    texto = blocks.CharBlock(
        required=True,
        label="Texto da Fonte",
        help_text="Texto que aparecerá clicável (ex: CNN, Reuters, BBC)"
    )
    link = blocks.URLBlock(
        required=True,
        label="URL da Fonte",
        help_text="Link completo para a fonte (ex: https://www.cnnbrasil.com.br/...)"
    )
    
    class Meta:
        icon = "link"
        label = "Fonte com Link"
        template = "content/blocks/fonte_link_block.html"
```

### Template HTML

```html
<div class="fonte-link-block my-3">
    <p class="mb-0">
        Fonte: <a href="{{ value.link }}" 
                  target="_blank" 
                  rel="noopener noreferrer"
                  style="color: #E3120B; text-decoration: none; font-weight: 500;">{{ value.texto }}</a>
    </p>
</div>
```

## Atributos do Link

- `target="_blank"`: Abre o link em uma nova aba
- `rel="noopener noreferrer"`: Segurança adicional ao abrir em nova aba
- `style="color: #E3120B"`: Cor vermelha do site
- `style="text-decoration: none"`: Remove o sublinhado
- `style="font-weight: 500"`: Peso semi-bold

## Lista de Blocos Disponíveis

Com a adição do FonteLinkBlock, os blocos disponíveis no ArticlePage são:

1. Parágrafo
2. Título/Subtítulo
3. Imagem (Somente Upload)
4. Imagem (Upload ou URL)
5. GIF Animado
6. Áudio/Podcast
7. Download PDF
8. Vídeo (YouTube, Vimeo, etc.)
9. Citação
10. Lista
11. Divisor
12. **Fonte com Link** (NOVO)
13. HTML Customizado

## Notas de Segurança

- O campo `link` é validado automaticamente pelo `URLBlock` do Wagtail
- O atributo `rel="noopener noreferrer"` previne vulnerabilidades de segurança ao abrir links em novas abas
- Apenas usuários com permissões de admin podem adicionar este bloco

## Testes

O bloco foi testado e validado:
- ✅ Importação do modelo funciona corretamente
- ✅ Campos são renderizados no admin
- ✅ Template renderiza o HTML esperado
- ✅ Links externos são validados
- ✅ Todos os testes existentes continuam passando

## Changelog

### 2025-10-13
- Criação inicial do FonteLinkBlock
- Adição ao StreamField do ArticlePage
- Criação do template de renderização
- Criação da migration 0019
- Documentação completa
