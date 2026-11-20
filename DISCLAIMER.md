# Aviso importante (leia antes de usar)

O Garimpo é um software livre, entregue **"como está", sem garantia de nenhum tipo** (veja a [licença](LICENSE)).
Ao usar, você assume todos os riscos descritos aqui. Isto não é aconselhamento jurídico.

## 1. O WhatsApp conectado é NÃO oficial

O Garimpo conecta ao seu WhatsApp por meio de um cliente de código aberto
([go-whatsapp-web-multidevice](https://github.com/aldinokemal/go-whatsapp-web-multidevice), baseado na biblioteca
[whatsmeow](https://github.com/tulir/whatsmeow)). **Esse tipo de conexão não é autorizado nem aprovado pelo WhatsApp/Meta.**

Consequências possíveis:

- o WhatsApp pode **derrubar a sessão** a qualquer momento (você precisará ler o QR code de novo);
- o WhatsApp pode **restringir** o número (impedir conversas novas) ou **bloqueá-lo temporária ou definitivamente**;
- mensagens podem deixar de chegar ou de ser entregues.

**Se o seu WhatsApp cair, for restringido ou banido, nem o Garimpo, nem quem o publicou, nem os autores dos
componentes de terceiros têm culpa ou responsabilidade.** Você decidiu usar.

Para reduzir o risco (não eliminar):

- use um número que você aceite arriscar, de preferência **não** o seu número pessoal ou o único canal do seu negócio;
- comece devagar: 20 a 30 mensagens por dia, com intervalos de alguns minutos, só em horário comercial;
- não mande para quem não tem relação com o seu serviço e **pare de contatar quem pedir** (o Garimpo descarta quem
  responde "não tenho interesse", "pare" ou parecido, mas a responsabilidade é sua);
- o Garimpo pausa os disparos sozinho se o WhatsApp avisar de restrição ou bloqueio. Quando isso aparecer, **não
  religue** antes de entender o motivo.

### O ideal é usar o WhatsApp oficial

O caminho autorizado e seguro para mensagens em volume é a **WhatsApp Business Platform** (a API oficial da Meta).
Ela tem custo, exige aprovação de modelos de mensagem e regras de consentimento (opt-in), mas é a única forma que a
Meta apoia. **O Garimpo ainda não integra a API oficial.** Se o seu negócio depende do WhatsApp, use a oficial.

## 2. Google Maps

O motor de busca lê páginas do Google Maps. Isso pode contrariar os termos de uso do Google. Seu endereço de IP pode
ser limitado ou bloqueado temporariamente. Use com moderação e por sua conta e risco.

## 3. Dados pessoais, LGPD e mensagens comerciais não solicitadas

Os dados coletados são públicos, mas podem incluir dados pessoais (nome de dono, telefone de MEI, e-mail). Você é o
responsável por:

- ter uma base legal para o contato (por exemplo, legítimo interesse, com avaliação própria);
- oferecer uma forma simples de a pessoa pedir para não ser mais contatada, e respeitar o pedido;
- cumprir a LGPD e as demais leis do seu país sobre contato comercial e consumo.

Não use o Garimpo para spam, golpe, assédio ou qualquer coisa ilegal.

## 4. Seus dados e sua sessão ficam no seu computador

- `data/`: banco de leads, configurações, senhas geradas e páginas de diagnóstico.
- `gateway/data/`: **a sessão do seu WhatsApp** e uma **cópia do histórico das suas conversas**.

Trate essas pastas como senhas. **Nunca as envie ao GitHub** (o `.gitignore` já as exclui), não as compartilhe e
proteja o computador com senha. Para revogar o acesso do Garimpo ao seu WhatsApp, abra o WhatsApp no celular em
**Configurações, Aparelhos conectados** e desconecte o aparelho "Garimpo".

## 5. Sem suporte garantido

Os autores não garantem que o Garimpo funcione, continue funcionando ou seja adequado ao seu uso. Os componentes de
terceiros podem mudar ou parar de funcionar a qualquer momento (o WhatsApp e o Google mudam seus sistemas com
frequência).
