# Processo Seletivo Visio Infraestrutura de Software
João Pedro Trevisan
Agosto de 2024

---
## Para rodar o projeto
O arquivo requirements.txt serve de base para que o utilitario pip baixe as dependências necessárias. Basta rodar `pip requirements.txt`

### Analise de dados
A parte de analise deste trabalho foi feita no notebook python chamado Analise_encoding.ipynb, nele se encontra explicações detalhadas dos experimentos e de suas conclusões. A bateria de testes realizada fez uso das funções dentro da pasta utils no arquivo test_reencoders.py.

### API
A API foi implementada fazendo uso de uvicorn e para rodá-la basta estar na raiz do projeto e usar o comando `uvicorn api:app`

## Compilação do ffmpeg
Para que possamos converter vídeos para os codecs VP8 e VP9 precisamos compilar o ffmpeg com uso das bibliotecas `lbvpx` e para fazer o reencoding para AV1 é necesaária a biblioteca `libaom`.  Desta forma, os passos a seguir adaptados a partir do guia da [wiki do ffmpeg](https://trac.ffmpeg.org/wiki/CompilationGuide/Ubuntu) são necessários para construir o programa a ser usado em distribuições linux baseadas em Debian:

**Baixar as dependências**:
```
apt-get update -qq && apt-get -y install \
  autoconf \
  automake \
  build-essential \
  cmake \
  git-core \
  libgnutls28-dev \
  libass-dev \
  libfreetype6-dev \
  libgnutls28-dev \
  libmp3lame-dev \
  libsvtav1-dev \
  libsvtav1enc-dev \
  libsdl2-dev \
  libtool \
  libva-dev \
  libvdpau-dev \
  libvorbis-dev \
  libxcb1-dev \
  libxcb-shm0-dev \
  libxcb-xfixes0-dev \
  meson \
  ninja-build \
  pkg-config \
  texinfo \
  wget \
  yasm \
  zlib1g-dev
```

**Criação da pasta de instalação na /home do usuário**:  
```
mkdir -p ~/ffmpeg_sources ~/bin
```

**Download e construção do libvpx**:
```
cd ~/ffmpeg_sources && \
sudo git -C libvpx pull 2> /dev/null || sudo git clone --depth 1 https://chromium.googlesource.com/webm/libvpx.git && \
cd libvpx && \
sudo PATH="$HOME/bin:$PATH" ./configure --prefix="$HOME/ffmpeg_build" --disable-examples --disable-unit-tests --enable-vp9-highbitdepth --as=yasm && \
sudo PATH="$HOME/bin:$PATH" make && \
sudo make install
```

**Download e construção da libaom**:
```
cd ~/ffmpeg_sources && \
sudo git -C aom pull 2> /dev/null || sudo git clone --depth 1 https://aomedia.googlesource.com/aom && \
sudo mkdir -p aom_build && \
cd aom_build && \
sudo PATH="$HOME/bin:$PATH" cmake -G "Unix Makefiles" -DCMAKE_INSTALL_PREFIX="$HOME/ffmpeg_build" -DENABLE_TESTS=OFF -DENABLE_NASM=on ../aom && \
sudo PATH="$HOME/bin:$PATH" make && \
sudo make install
```

**Compilação do FFmpeg com as devidas bibliotecas**:
```
cd ~/ffmpeg_sources && \
sudo wget -O ffmpeg-snapshot.tar.bz2 https://ffmpeg.org/releases/ffmpeg-snapshot.tar.bz2 && \
sudo tar xjvf ffmpeg-snapshot.tar.bz2 && \
cd ffmpeg && \
sudo PATH="$HOME/bin:$PATH" PKG_CONFIG_PATH="$HOME/ffmpeg_build/lib/pkgconfig" ./configure \
  --prefix="$HOME/ffmpeg_build" \
  --pkg-config-flags="--static" \
  --extra-cflags="-I$HOME/ffmpeg_build/include" \
  --extra-ldflags="-L$HOME/ffmpeg_build/lib" \
  --extra-libs="-lpthread -lm" \
  --ld="g++" \
  --bindir="$HOME/bin" \
  --enable-gpl \
  --enable-gnutls \
  --enable-libaom \
  --enable-libass \
  --enable-libfreetype \
  --enable-libmp3lame \
  --enable-libsvtav1 \
  --enable-libvorbis \
  --enable-libvpx \
  --enable-nonfree && \
sudo PATH="$HOME/bin:$PATH" make && \
sudo make install && \
hash -r
```

**Comandos para deletar esta compilação se for necessário**:
```
sudo rm -rf ~/ffmpeg_build ~/ffmpeg_sources ~/bin/{ffmpeg,ffprobe,ffplay,x264,x265,nasm}
sed -i '/ffmpeg_build/d' ~/.manpath
hash -r
```
**Comandos para deletar as dependências baixadas**:
```
sudo apt-get autoremove autoconf automake build-essential cmake git-core libgnutls28-dev libass-dev libfreetype6-dev libgnutls28-dev libmp3lame-dev libsvtav1-dev libsvtav1enc-dev libsdl2-dev libtool libva-dev libvdpau-dev libvorbis-dev libxcb1-dev libxcb-shm0-dev libxcb-xfixes0-dev meson ninja-build pkg-config texinfo wget yasm zlib1g-dev
```

