# mtcli-trade
  
*mtcli-trade* é um plugin para o projeto [mtcli](https://github.com/vfranca/mtcli) que permite *executar ordens de compra e venda no MetaTrader 5 via terminal*, com foco em *acessibilidade para pessoas com deficiência visual*.
  
---
  
## Funcionalidades
  
- Envio de ordens *BUY* e *SELL*
- Suporte a ordens *a mercado* e *limitadas*
- Parâmetros ajustáveis de:
  - *Lote*
  - *Stop Loss (SL)* em pontos
  - *Take Profit (TP)* em pontos
- Exportação e logs acessíveis
- Compatível com leitores de tela
  
---
  
## Público-alvo
  
Desenvolvido com foco em *traders cegos ou com baixa visão*, mas útil também para quem prefere trabalhar via linha de comando ou automatizar operações.
  
---
  
## Instalação
  
Pré-requisitos
  
- Windows com MetaTrader 5 instalado
- Python 3.10 a 3.13

  
```bash
pip install mtcli-trade
```
  
Ou, via Poetry:

```bash
poetry add mtcli-trade
```
  
---
  
## Exemplos de uso
  
Comprar a mercado
  
```bash
mt buy --symbol WINV25 --lot 1 --sl 100 --tp 300
```
  
Vender com ordem limitada
  
```bash
mt sell --symbol WINV25 --lot 1 --limit --preco 123000
```
  
---
  
## Testes e simulações
  
O plugin pode ser testado com:
- Dados reais do MetaTrader 5
- Simuladores de resposta (mock da API)
  
Consulte a seção tests/ do repositório para detalhes.
  
---
  
## Aviso
  
> Teste sempre em conta demo antes de operar no mercado real.
  
---
  
## Licença
  
Distribuído sob licença GPL-3.0.
  
---
  
Para mais detalhes, veja a [documentação do projeto mtcli](https://vfranca.github.io/mtcli).
