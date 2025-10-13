# Guia de Customização do Rodapé

## Visão Geral

A partir da versão mais recente, o site agora permite personalizar a frase que aparece no rodapé através do painel administrativo do Wagtail.

## Como Usar

### Acessando as Configurações

1. Faça login no painel administrativo do Wagtail: `/admin/`
2. Navegue até **Páginas** no menu lateral
3. Clique na página **Início** (HomePage)
4. Clique em **Editar**

### Configurando o Rodapé

Na seção **Configurações do Rodapé**, você encontrará dois campos:

#### 1. Frase do Rodapé
- **Campo:** Texto livre (até 200 caracteres)
- **Padrão:** "Reconstruindo o sentido no fim da era antiga."
- **Descrição:** O texto que aparece no rodapé do site, logo abaixo do nome do portal

**Exemplo de uso:**
```
Análise profunda dos acontecimentos que moldam nosso tempo.
```

#### 2. Tamanho da Frase do Rodapé
- **Campo:** Dropdown com opções pré-definidas
- **Padrão:** Pequeno (0.7rem)
- **Opções disponíveis:**
  - Muito Pequeno (0.6rem)
  - Pequeno (0.7rem) - Padrão
  - Médio (0.8rem)
  - Grande (0.9rem)
  - Muito Grande (1rem)
  - Extra Grande (1.1rem)

### Validação

O sistema valida automaticamente:
- ✅ A frase deve ter pelo menos 10 caracteres
- ✅ Não pode exceder 200 caracteres
- ✅ Espaços em branco são removidos automaticamente

### Visualização

Após salvar as alterações:
1. Clique em **Publicar** no canto superior direito
2. As mudanças serão refletidas imediatamente em todo o site
3. A frase aparecerá no rodapé de todas as páginas

## Onde a Frase Aparece

A frase customizada aparece em:
- ✅ Todas as páginas do site
- ✅ Página inicial
- ✅ Páginas de artigos
- ✅ Páginas de seções
- ✅ Páginas de suporte

## Localização no Código

Para desenvolvedores que precisam entender ou modificar esta funcionalidade:

### Model (Backend)
```python
# content/models.py
class HomePage(Page):
    footer_tagline = models.CharField(
        max_length=200,
        default="Reconstruindo o sentido no fim da era antiga.",
        verbose_name="Frase do Rodapé",
    )
    
    footer_tagline_size = models.CharField(
        max_length=20,
        choices=TAGLINE_SIZE_CHOICES,
        default='0.7rem',
        verbose_name="Tamanho da Frase do Rodapé",
    )
```

### Template (Frontend)
```html
<!-- templates/footer.html -->
<p class="text-white-50 mb-3" 
   style="font-size: {{ home_page.footer_tagline_size }};">
    {{ home_page.footer_tagline }}
</p>
```

### Context Processor
```python
# content/context_processors.py
def home_page_settings(request):
    """Disponibiliza home_page em todos os templates"""
    home_page = HomePage.objects.live().first()
    return {'home_page': home_page}
```

## Troubleshooting

### A frase não aparece
1. Verifique se você clicou em **Publicar** após editar
2. Limpe o cache do navegador (Ctrl+F5)
3. Verifique se a HomePage está ativa e publicada

### O tamanho não muda
1. Certifique-se de que salvou e publicou as alterações
2. Limpe o cache do navegador
3. Verifique o console do navegador para erros de CSS

### Erro de validação
- Se você receber um erro, verifique se:
  - A frase tem pelo menos 10 caracteres
  - A frase não excede 200 caracteres
  - Você preencheu o campo

## Ajustes Manuais de Espaçamento

Se você precisar ajustar o espaçamento do corpo da página ou das seções manualmente:

### Espaçamento do Header
**Arquivo:** `templates/header.html`
```html
<!-- Linha ~124 -->
<div style="height: 105px;"></div>
```
- Aumente o valor para mais espaço abaixo do header
- Diminua para menos espaço

### Espaçamento de Seções
**Arquivo:** `static/css/custom.css`
```css
.section-header {
    padding-top: 2.1rem;  /* Ajuste este valor */
    margin-top: 1.4rem;   /* Ajuste este valor */
}
```

### Espaçamento Mobile
```css
@media (max-width: 768px) {
    .section-header {
        padding-top: 1.5rem;  /* Ajuste para mobile */
        margin-top: 1rem;
    }
}
```

## Dicas de Uso

### Melhores Práticas
- ✅ Use frases curtas e impactantes (máximo 100 caracteres)
- ✅ Evite jargões técnicos difíceis de entender
- ✅ Mantenha consistência com a identidade do site
- ✅ Teste em diferentes dispositivos após alterar o tamanho

### Exemplos de Boas Frases
```
✅ "Reconstruindo o sentido no fim da era antiga."
✅ "Análise profunda dos acontecimentos globais."
✅ "Jornalismo de qualidade para tempos complexos."
✅ "Compreendendo o mundo através da análise crítica."
```

### Exemplos a Evitar
```
❌ "Lorem ipsum dolor sit amet..." (sem significado)
❌ "Clique aqui!!!" (muito informal/spam)
❌ "LEIA AGORA!!!" (caps lock excessivo)
❌ Textos muito longos que não cabem bem
```

## Histórico de Mudanças

### v1.0 (2025-10-13)
- ✨ Adicionada customização de texto do rodapé
- ✨ Adicionada opção de tamanho da frase
- ✨ Validação automática de tamanho
- ✨ Context processor para disponibilizar globalmente
- ✨ Redução de espaçamento do corpo em 30%

---

**Para mais informações:** Consulte a documentação principal ou entre em contato com a equipe de desenvolvimento.
