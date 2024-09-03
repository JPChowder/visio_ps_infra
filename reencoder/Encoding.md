# Guia de seleção de parâmetros para encoding

---
## Geral
Em um primeiro momento será listada uma série de parâmetros que podem ser alterados para quando for realizado o reencode de um vídeo. Junto de cada parâmetro haverá uma breve explicação e um porquê de se usar ou não usar:
1. **Bit Rate**
	- O bit rate é um dos fatores que mais impacta a qualidade do vídeo, principalmente durante cenas complexas onde muitas coisas acontecem por toda a tela. Quando não determinado, o a conversão é feita em modo de qualidade constante, onde se tenta não perder dados no reencoding, informá-lo pode aumentar a quantidade de informações (subindo o bit rate) ou colocar o reencoder em modo de qualidade limitada, onde o bit rate informado será o limitante superior para conversões de bitrate variável.
2. **Constant/Variable Rate Factor**
	- O bit rate não precisa ser constante, pode-se alterar dinamicamente a taxa de bits para que seja fornecida maior banda em momentos mais complexos do vídeo. Assim sendo, **sempre optaremos** por fatores variáveis da taxa de bits.
3. **Resolution**
	- Este parâmetro poderia diminuir significativamente o peso dos vídeos, contudo diminuir o tamanho da imagem pode impactar significativamente a funcionalidade dos modelos de IA que atuam sobre ele e assim sendo **não será utilizado**.
4. **Frame Rate**
	- Semelhante com a questão da resolução, pode ser uma fonte de economia de espaço de armazenamento e de banda para transferência, contudo pode impactar o desempenho da solução de IA e diminuir a legibilidade das imagens para humanos. **Não será usado**.
5. **Speed/Preset**
	- Este parâmetro oferece uma opção de velocidade em que o encoder tentará finalizar o trabalho. Velocidades maiores tendem a criar resultados piores pois há menos tempo para otimizações.

## VP8
Por padrão este codec define o uso de **bit rate variável**, o valor informado será a média do bit rate ao longo do vídeo todo. Existe como alternativa o parâmetro **CRF** que aceita valores de 0 ~ 63 e buscará fazer com que cada frame tenha bitrate o suficiente ao invés de mirar em uma média geral, com esta opção o bitrate informado na opção `-b:v [bitrate]` será o máximo permitido.

Ainda sobre o bit rate, pode-se fazer uso das opções `qmin` (default 4, range 0 ~ 63) e `qmax` (dafault 63, range `qmin` ~ 63) para colocar um valor mínimo e um máximo para que o encoder tenha um alcance dentro do qual pode determinar a qualidade.

Pode-se ainda fazer uso de um bit rate constante, que não garante que todos frames terão a mesma quantidade de bits, mas faz com que esta taxa esteja bastante controlada. Geralmente é usado para garantir um certo tamanho de arquivo ou para streaming em canais que só aceitam um determinado bit rate.

## VP9 
O encoder VP9 oferece por padrão o bit rate variável onde tentará alcançar uma determinada taxa de bits na média, bem como o VP8. Assim como no seu predecessor este modo oferece pouco controle sobre a qualidade e não é eficiente em relação a compressão do encoder.

As outras opções para este codec são **two-pass**, **constant quality**, **constrained bit rate** e **constant bit rate**.

No primeiro modo existem duas maneiras de se fazer o encoding, a primeira das quais tentará manter um bit rate médio especificado e a segunda faz uso do parâmetro `-crf` que buscará manter um certo padrão de qualidade de acordo com o valor determinado.

O modo de qualidade constante faz uso apenas do `-crf` buscando uma certa qualidade perceptiva do material. Este encoder da preferência para o modo de duas passadas, mas fazer com apenas uma pode economizar tempo e exigir menos recursos de processamento.

A opção de *constrained quality* faz uso do parâmetro de `-crf` e de um teto máximo para o bit rate ou então de um "teto" e um "chão" criando um alcance dentro do qual a taxa de bits deve ficar.

A opção de constant bit rate é boa para quando se quer manter um certo tamanho de arquivo ou para quando se faz streaming por canais que só aceitam um determinado bit rate. Para acessá-la basta usar os parâmetros `-minrate` e `-maxrate` com valores iguais. O bit rate não será perfeitamente constante, mas será próximo.

O VP9 tem **presets** que vem em três tipos: `good`, `best` e `realtime`, onde os dois primeiros trazem um resultado um tempo menor com qualidade menor e num tempo maior com qualidade maior respectivamente. O problema com presets é perder o controle de ajuste fino do processo que se está implementando.

Por fim, o VP9 oferece uma opção ***lossless*** que promete uma conversão sem perdas de qualidade.

## AV1
Existem 3 formas de ter acesso a este codec através do ffmpeg e elas são as bibliotecas `libaom-av1`, `libsvtav1` e `librav1e`. Para o nosso caso faremos uso da biblioteca `libaom-av1`.

Para o encoding com uso desta biblioteca temos 4 opções de alteração de bit rate: **constant quality**, **constrained quality**, **2-pass average bit rate** e **1-pass average bit rate**.

A primeira é usada por meio do parâmetro de `-crf` sem outra indicação extra.

A segunda, além do parâmetro de `-crf` deve receber um limite de bit rate maior que zero após o parâmetro `-b:v`.

A opção de duas passadas é semelhante à  maneira de se trabalhar com o codec VP9, salvo que não se especifica um `-crf` para as passadas.

Por fim, a última opção é a mais comum pois faz uso de um valor médio a ser mantido pelo bit rate através do uso exclusivo do parâmetro `-b:v [bit rate]`.

O encoder AV1 possui também 3 presets que são `quality quality`, `quality balanced` e `quality speed`, tendo velocidades de renderização cada vez maiores e qualidades de imagem cada vez piores.

