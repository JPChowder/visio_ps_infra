import subprocess
import os
import json

class MetaFetch:
    """
    Classe utilizada pra colher metadados de videos por meio do comando ffprobe.
    """
    def __init__(self, video_path):
        self.video_path = video_path
        self.info = self.get_video_info()

    # metodo que chama o ffprobe com os parametros adequados e retorna erro caso o comando tenha problemas
    def get_video_info(self):
        """
        Método que colhe informacoes do video a ser avaliado. Faz uso do comando:
        ffprobe -v error -select_streams v:0 -show_entries stream=bit_rate,r_frame_rate,duration,codec_name -of json [caminho_do_video]

        Returns:
            Retorna a saida do comando ffprobe no formato json.

        Raises:
            CalledProcessError: retorna a saida em stderr do comando.
        """
        ffprobe_cmd = [
        'ffprobe', 
        '-v', 'error', 
        '-select_streams', 'v:0', 
        '-show_entries', 'stream=bit_rate,r_frame_rate,duration,codec_name',
        '-of', 'json',
        self.video_path
        ]
        try:
            result = subprocess.run(ffprobe_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
            return json.loads(result.stdout)
        except subprocess.CalledProcessError as e:
            print(f"Falha ao colher dados do video! Erro: {e.stderr.decode()}")
            return None

    # Bitrate em Bits/s
    def get_bitrate(self):
        """
        Metodo getter que retorna a taxa de bits por segundo do video examinado.

        Returns:
            bitrate_bps (str): Video Bps
        """
        bitrate_bps = int(self.info['streams'][0].get('bit_rate', 0))
        #bitrate_kbps = bitrate_bps / 1000
        return str(bitrate_bps)
    
    # Duracao em minutos
    def get_duration(self):
        """
        Metodo getter que retorna a duracao em segundos do video examinado.

        Returns:
            duration_min (int): Duracao do video em minutos com 2 casas decimais.
        """
        duration_sec = float(self.info['streams'][0].get('duration', 0.0))
        duration_min = duration_sec / 60
        return round(duration_min,2)
    
    # Frames por seguindo
    def get_frame_rate(self):
        """
        Metodo getter que retorna a taxa de quadros segundo do video examinado.

        Returns:
            num / denom (int): Taxa de num frames por denom segundos do video.
        """
        r_frame_rate = self.info['streams'][0].get('r_frame_rate', '0/1')
        num, denom = map(int, r_frame_rate.split('/'))
        return num / denom

    # Codec do video
    def get_encoding(self):
        """
        Metodo getter que retorna o codec do video examinado.

        Returns:
            video_codec (str): Nome do codec do video.
        """
        return self.info['streams'][0].get('codec_name', 'Unknown')

    # Tamanho em bytes
    def get_size(self):
        """
        Metodo getter que retorna o tamanho em bytes video examinado.

        Returns:
            sizze_bytes (int): Tamanho em bytes do video.
        """
        size_bytes = os.path.getsize(self.video_path)
        #size_Mbytes = size_bytes / 1000000
        return size_bytes

# Exemplos:
# video = MetaFetch('path_to_your_video.mp4')
# print(video.get_bitrate())
# print(video.get_duration())
# print(video.get_frame_rate())
# print(video.get_encoding())
# print(video.get_size())