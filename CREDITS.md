# Créditos

O Garimpo existe porque outras pessoas construíram e abriram o código das peças mais difíceis. Todo o mérito delas
é delas. Se este projeto te serve, **dê uma estrela nos repositórios abaixo**.

## Componentes que o instalador baixa (não são redistribuídos neste repositório)

O `install.py` baixa cada um direto da fonte original, preso a uma versão exata e conferido por hash.

### Motor de busca do Google Maps: google-maps-scraper-kit

- Autor: **Mahan** ([@Mahanaicoach](https://github.com/Mahanaicoach)) · licença **MIT**
- https://github.com/Mahanaicoach/google-maps-scraper-kit
- Faz a busca no Google Maps com um Chrome sem janela, devolve nome, telefone, site, avaliações e coordenadas, e
  procura e-mails e redes sociais nos sites. O Garimpo usa a API de jobs dele.
- O kit, por sua vez, credita (veja o `CREDITS.md` dele): **gosom/google-maps-scraper** (Georgios Komninos, MIT), cuja
  API de jobs e colunas de CSV ele mantém; **OpenLeadFinder** (MIT); a lista de cidades **GeoNames** (CC BY 4.0); a
  lista de categorias de **lobstr.io**; e o **Chrome for Testing** do Google.

### Gateway do WhatsApp: go-whatsapp-web-multidevice

- Autor: **Aldino Kemal** ([@aldinokemal](https://github.com/aldinokemal)) e colaboradores · licença **MIT**
- https://github.com/aldinokemal/go-whatsapp-web-multidevice (binário oficial da release v9.9.0)
- É o "módulo do WhatsApp": conecta o seu número por QR code, envia e recebe mensagens e avisa o Garimpo por webhook.
- Construído sobre a **whatsmeow**, de **Tulir Asokan** ([@tulir](https://github.com/tulir)), licença **MPL-2.0**:
  https://github.com/tulir/whatsmeow (a mesma biblioteca usada pelas pontes de WhatsApp do projeto Matrix).

## Projetos estudados como referência de recursos

Olhamos o que estes projetos entregam para decidir o que o Garimpo deveria ter. **Nenhum código deles foi copiado.**

- **gosom/google-maps-scraper**: Georgios Komninos · MIT · https://github.com/gosom/google-maps-scraper
- **omkarcloud/google-maps-scraper**: Chetan Jain · MIT · https://github.com/omkarcloud/google-maps-scraper
- **Mahanaicoach/google-maps-scraper-kit**: citado acima.

## Alternativa suportada

- **Evolution API** ([EvolutionAPI/evolution-api](https://github.com/EvolutionAPI/evolution-api)) e a biblioteca
  **Baileys** ([WhiskeySockets/Baileys](https://github.com/WhiskeySockets/Baileys), MIT): o Garimpo também sabe falar
  com uma Evolution que você já tenha. Não é incluída nem instalada.

## Carregado pelo navegador (não incluído)

- **Leaflet** 1.9.4: Volodymyr Agafonkin e colaboradores · BSD-2-Clause · https://leafletjs.com
- **OpenStreetMap**: © colaboradores do OpenStreetMap · dados sob [ODbL](https://www.openstreetmap.org/copyright).
  O mapa usa os blocos públicos do `tile.openstreetmap.org`, que têm uma
  [política de uso](https://operations.osmfoundation.org/policies/tiles/) para uso leve. Para uso intenso, troque
  por um provedor de mapas seu.
- **Overpass API**: usada para buscar os bairros de uma cidade (dados do OpenStreetMap, ODbL), com cache em disco.
- **Fontes**, via Google Fonts, todas sob a SIL Open Font License: **Inter** (Rasmus Andersson),
  **JetBrains Mono** (JetBrains), **Space Grotesk** (Florian Karsten).

## IA opcional e ferramentas de desenvolvimento

- A análise com IA usa o **Claude Code** ([Anthropic](https://www.anthropic.com)) que você já tenha instalado e
  logado (comando `claude`). Sem ele, o resto funciona normalmente.
- Este projeto foi desenvolvido com a ajuda do **Claude Code**, incluindo a skill de visualização de dados `dataviz`
  que acompanha a ferramenta, usada para o desenho dos gráficos.

## Este projeto

O código do Garimpo (`garimpo.py`, `diag.py`, `web/`, `install.py`) está sob a licença [MIT](LICENSE).
Veja também o [aviso importante](DISCLAIMER.md).

Encontrou algum crédito faltando ou errado? Abra uma issue que eu corrijo.
