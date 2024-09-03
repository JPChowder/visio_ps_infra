from .video_reencoder import VideoReencoder
import subprocess

class VP8Reencoder(VideoReencoder):
    def reencode(self):
        """
        Realiza o reencoding de um video para o codec VP8 por meio da biblioteca libvpx.

        Args:
            input_file (str): Caminho para o video a ser convertido.
            output_file (str): Caminho para o novo video convertido.
            crf (int): Consant (bit) Rate Factor. Valores de 0 ~ 63, qualidade inversamente proporcional. 
            speed/preset (int): Velocidade que o ffmpeg fara a conversao. Aceita valores de 0 ~ 4, velocidade proporcional.
            threads (int): Quantidade de threads a serem usadas. Default = 2.
            bitrate (str): Taxa de bits para cada quatro. Default = None -> qualidade sem perdas.

        Returns:
            Sem retornos da funcao. Rende um video convertido no caminho informado.
        """
        self._run_ffmpeg_command('libvpx')

    def _run_ffmpeg_command(self, codec):
        command = [
            'ffmpeg', '-i', self.input_file,
            '-c:v', codec,
            '-crf', str(self.crf),
            '-speed', str(self.speed),
            '-threads', '2'
        ]

        # Adicionar o bitrate se for especificado (constrained quality)
        if self.bitrate:
            command.extend(['-b:v', self.bitrate])

        command.append(self.output_file)
        subprocess.run(command, check=True)