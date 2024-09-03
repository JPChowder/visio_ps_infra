from abc import ABC, abstractmethod
import subprocess

class VideoReencoder(ABC):
    """
    Classe abstrata para servir de base aos reencoders especificos.
    """
    def __init__(self, input_file, output_file, crf, speed, threads=2, bitrate=None):
        self.input_file = input_file
        self.output_file = output_file
        self.crf = crf
        self.speed = speed
        self.threads = threads
        self.bitrate = bitrate

    @abstractmethod
    def reencode(self):
        """
        Realiza o reencoding de um video para outro codec.

        Args:
            input_file (str): Caminho para o video a ser convertido.
            output_file (str): Caminho para o novo video convertido.
            crf (int): Consant (bit) Rate Factor. Valores de 0 ~ 63, qualidade inversamente proporcional. 
            speed (int): Velocidade que o ffmpeg fara a conversao.
            threads (int): Quantidade de threads a serem usadas. Default = 2.
            bitrate (str): Taxa de bits para cada quatro. Default = None -> qualidade sem perdas.

        Returns:
            Sem retornos da funcao. Rende um video convertido no caminho informado.
        """
        pass

    def _run_ffmpeg_command(self, codec):
        command = [
            'ffmpeg', '-i', self.input_file,
            '-c:v', codec,
            '-crf', str(self.crf),
            '-speed', str(self.speed),
            '-threads', str(self.threads),
        ]

        if self.bitrate:
            command.extend(['-b:v', self.bitrate])

        command.append(self.output_file)
        subprocess.run(command, check=True)