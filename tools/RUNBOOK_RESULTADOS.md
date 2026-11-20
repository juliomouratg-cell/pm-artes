# Runbook: post de RESULTADO do jogo do bicho (Rio) no @professordamilhar

Roda 6x por dia (9h40, 11h40, 14h40, 16h40, 18h40, 21h40, horário de Maceió/Brasília).
Objetivo: pegar o resultado da extração que acabou de sair, gerar o card e agendar no Metricool para daqui ~10 min.

## Extrações (Rio de Janeiro)
| Código no card | Hora | Roda às |
|---|---|---|
| PPT | 09h20 | 09h40 |
| PTM | 11h20 | 11h40 |
| PT | 14h20 | 14h40 |
| PTV | 16h00 | 16h40 |
| PTN | 18h20 | 18h40 |
| CORUJINHA | 21h20 | 21h40 |
| FEDERAL | 19h00 (só quarta e sábado) | junto com a de 21h40 |

## Passos
1. Repositório `juliomouratg-cell/pm-artes` (precisa de push). Leia `resultados/postados.json` (lista de "AAAA-MM-DD_EXTRACAO" já postados). Descubra qual extração de HOJE já deveria ter saído e ainda não foi postada (pode ser mais de uma se uma rodada anterior falhou; nesse caso faça todas, mais antiga primeiro).
2. Resultado: no Chrome do usuário (Claude in Chrome), abra uma aba nova em
   `https://www.resultadofacil.com.br/resultado-do-jogo-do-bicho/RJ` e leia com get_page_text.
   Confira que a data da página é a de hoje. Pegue os 7 prêmios (milhar do 1º ao 5º, 6º soma, 7º multiplicação).
   O site chama a das 09h20 de "PT" e a das 21h20 de "Coruja": no card use PPT e CORUJINHA.
   Federal: procure a Federal do dia no mesmo site (ou na Caixa) e use os 5 prêmios (últimos 4 dígitos).
   Se ainda não saiu, espere 5 min e tente de novo (até 3 vezes). Se não sair, pule e deixe para a próxima rodada.
   NUNCA invente número. Copie exatamente o que está na página.
3. Gere o card: crie `resultados/AAAA-MM-DD_EXT.json` no formato
   `{"data":"2026-11-20","extracao":"PTM","hora":"11h20","premios":["0746","9974","4209","7883","6369","9181","440"]}`
   e rode `python3 tools/resultado.py resultados/AAAA-MM-DD_EXT.json resultados/RES_AAAA-MM-DD_EXT.mp4`
   (gera também o .txt com a legenda). Precisa de playwright+chromium e ffmpeg; instale se faltar.
   Confira o PNG em /tmp/res.png antes de seguir (grupo do 1º deve bater com o site).
4. git add/commit/push e confirme que `https://raw.githubusercontent.com/juliomouratg-cell/pm-artes/main/resultados/RES_...mp4` responde 200.
5. Metricool no Chrome: `https://app.metricool.com/planner/calendar?blogId=8228123&userId=6479798` (conta jesusitaju69).
   Se cair na tela de login, NÃO tente logar: avise o usuário (notificação) que precisa logar o Metricool no Chrome e pare.
   Criar publicação → ícone de mídia → "Adicionar vídeo" → aba "A partir do URL" → cole a URL raw → Aceitar (carrega a prévia) → Aceitar.
   Clique na caixa de texto e cole a legenda do .txt.
   Clique na data (embaixo, ao lado de Agendar): dia de hoje; hora e minuto são selects (clique e digite o número, Enter) = agora + 10 min.
   Clique Agendar. Confira na aba "Lista" que o post aparece como Pendente com a hora certa.
   Tire screenshot a cada passo; as coordenadas mudam com o tamanho da janela.
6. Acrescente "AAAA-MM-DD_EXT" em `resultados/postados.json`, commit e push. Feche as abas que você abriu.
7. Se algo falhar, mande notificação curta ao usuário dizendo qual extração não foi postada e por quê.
