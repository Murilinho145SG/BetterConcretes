# Screenshots para a página do CurseForge

Eu não rodo o client — estas são as capturas que você precisa fazer in-game e enviar para a página. Cada item tem: **nome do arquivo**, **conteúdo da cena**, **setup** para montar rápido no creative. Formato: PNG, F2 direto (tira de 1920×1080 ou 2560×1440). Sem shaders.

---

## 1. `01_hero_build.png` — imagem principal (topo da página)

**Cena**: uma casa/torre pequena com 3 cores fortes + 3 variantes misturadas. Contraste importa aqui.

**Setup**:
- Plat 12×12 de `smooth_light_gray_concrete`
- Paredes: `brick_red_concrete` alternado com `polished_red_concrete` em faixas horizontais
- Detalhes: 4 blocos de `chiseled_yellow_concrete` como "janelas"
- Câmera: isométrica 45° aérea, distância ~15 blocos

---

## 2. `02_palette_wall.png` — mostrar as 16 cores

**Cena**: muralha 16 blocos de largura × 4 de altura. Cada coluna = uma cor. Cada linha = uma variante (smooth, polished, chiseled, brick de baixo pra cima).

**Setup**: literalmente um muro. F3+B para desligar hitboxes. Câmera frontal reta, sem perspectiva estranha.

---

## 3. `03_ctm_wall.png` — prova visual do CTM

**Cena**: parede grande (pelo menos 8×8) de `smooth_gray_concrete` OU `smooth_cyan_concrete`. Mostrar que os blocos emendam sem costura visível.

**Setup**: depois monta uma segunda parede com `smooth_gray_concrete_powder` vanilla do lado, mesmo tamanho, pra comparação lado-a-lado. Duas fotos ou uma foto dividida.

**Caption sugerida**: "Connected textures (left) vs vanilla concrete (right)"

---

## 4. `04_chisel_gui.png` — GUI aberta

**Cena**: tela do Chisel aberta com `red_concrete` vanilla no slot de input. Mouse em cima do card "Polished" pra mostrar o tooltip. Output slot mostrando `polished_red_concrete`.

**Setup**: E pra inventário, clicar com o chisel num bloco existente ou usar o recipe direto. Captura com F1 para esconder HUD se quiser.

---

## 5. `05_jei_category.png` — JEI

**Cena**: tab de JEI aberta na categoria "Chiseling". Mostra vários ícones de chisel + seta + output, empilhados.

**Setup**: pressiona U em cima do chisel in-game ou digita "chisel" no search do JEI.

---

## 6. `06_creative_tab.png` — tab criativa

**Cena**: criativo aberto, aba "Better Concretes" selecionada, todos os 64 blocos visíveis (vai precisar de scroll, mas a primeira página já vende).

**Setup**: E + clicar no ícone da aba. Pega screenshot com o tooltip de um bloco aparecendo pra mostrar o nome ("Smooth Cyan Concrete").

---

## 7. `07_build_showcase.png` (opcional mas ajuda)

**Cena**: uma build livre sua, bonita, usando bastante variedade do mod. Vale uma estação, um monumento, um hall.

**Tempo**: ~20 min no creative flat world.

---

## Dicas rápidas

- **World**: cria um flat world, coloca no meio-dia fixo (`/time set 6000`, `/gamerule doDaylightCycle false`).
- **Tempo**: `/weather clear` pra nada de chuva/nuvem escurecer.
- **HUD**: F1 esconde inventário e crosshair. F3+B desliga hitboxes. F2 tira screenshot.
- **Naming**: rename os PNGs pra os nomes acima antes de subir no CurseForge — ajuda a manter ordem.
- **Ordem na página**: hero → palette → CTM → chisel GUI → JEI → creative tab → showcase.

Quando tiver as capturas, envia que eu monto a página final do CurseForge com as imagens no lugar certo.
