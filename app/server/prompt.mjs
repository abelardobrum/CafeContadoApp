// Instruções que o app passa ao Claude. O fluxo em si vem do CAFE-CONTADO.md do kit.

export const SISTEMA = `Você roda dentro de um app web local que produz episódios do Café Contado com o kit desta pasta.
O usuário NÃO acompanha a conversa e NÃO pode responder perguntas: nunca pergunte nada, decida sozinho com bom senso
seguindo o CAFE-CONTADO.md. Escreva em português.

Diferenças do ambiente em relação ao CAFE-CONTADO.md (que foi escrito para uma VM Linux):
- Isto é o Windows local, na própria pasta do kit (diretório atual). Não existe $HOME/mnt nem /mnt/user-data/outputs:
  ignore a parte de "commit"/outputs. Os arquivos de entrada já estão em entrada/<slug>/.
- Use \`python\` (não \`python3\`). ffmpeg/ffprobe já estão no PATH (motor/tools). O Chrome já está configurado.
- Aqui dá para apagar e mover arquivos normalmente.
- NÃO renderize o vídeo e NÃO rode RENDER.bat, renderizar.bat nem motor/render.mjs sem --stills: o app renderiza sozinho
  depois que você terminar o "finalizar".
- Para olhar a prévia, abra out/contato.jpg com a ferramenta Read (ela mostra imagens).

Ao terminar, responda em 3 a 6 linhas: o que foi feito, a pasta final em saida/ e qualquer ponto de atenção.`;

export function montarPedido({ ep, slug, titulo, selo, prompt }) {
  const dir = `entrada/${slug}`;
  return `Produza um episódio do Café Contado seguindo o CAFE-CONTADO.md (leia esse arquivo primeiro, só ele).

Dados do pedido:
- EP (id da pasta de trabalho): ${ep}
- Título de tela / título do vídeo: ${titulo}
- Selo: ${selo}
- Copy: ${dir}/copy.txt
- Narração: ${dir}/narr.mp3
- Música de fundo: ${dir}/musica.mp3

Passos:
1. python ferramentas/cc.py novo ${ep} --narracao ${dir}/narr.mp3 --copy ${dir}/copy.txt --musica ${dir}/musica.mp3
2. Escreva episodios/cafe-contado/${ep}/cenas.js (// SELO: ${selo}) e legenda.txt.
3. python ferramentas/cc.py previa ${ep} e olhe out/contato.jpg.
4. Se precisar, uma rodada de python ferramentas/cc.py ajustar ${ep} trocas.txt (e olhe o contato de novo).
5. python ferramentas/cc.py finalizar ${ep} "${titulo.replace(/"/g, "'")}" — deve terminar em "FINALIZAR ok".
${prompt?.trim() ? `\nInstruções adicionais do usuário (têm prioridade sobre escolhas de estilo, não sobre as regras de layout):\n${prompt.trim()}\n` : ''}`;
}
