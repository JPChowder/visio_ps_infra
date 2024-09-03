from .video_evaluator import VideoEvaluator
import subprocess

class PSNREvaluator(VideoEvaluator):

    def evaluate(self, video1_path: str, video2_path: str) -> float:
        """
        Calcula o PSNR entre dois videos por meio do ffmpeg.
        
        Args:
            video1_path (str): Caminho para o video original.
            video2_path (str): Caminho para o video convertido.
        
        Returns:
            float: A metrica de qualidade relativa entre os videos. 
        """
        command = [
            'ffmpeg', 
            '-i', video1_path, 
            '-i', video2_path, 
            '-lavfi', 'psnr', 
            '-f', 'null', 
            '-'
        ]
        # A saída deste comando vai para stderr ao inves de stdout, entao nesta chamada os parametros se invertem
        process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = process.communicate()
        
        # Por algum motivo, quando o metodo subprocess eh usado com a opcao 'text=True' eh impossivel se capturar
        # o texto para realizar uma manipulacao, o formato padrao deste texto depende de io.TextIOWrapper que 
        # depende de locale.getencoding. Em sistemas UNIX deveria ser retornado utf-8 e este passo de passar na 
        # forma de bytes e entao decodificar nao deveria ser necessario, contudo algo impede este caminho simples
        saida = stderr.decode('utf-8')
        
        # Processar a saida para buscar o valor medio
        output_lines = saida.splitlines()
        for line in reversed(output_lines):  # De baixo para cima pois o valor que buscamos eh um dos ultimos
            if "average:" in line:
                psnr_value = float(line.split("average:")[1].split()[0])
                return psnr_value
        
        raise ValueError("PSNR calculation failed: 'average' value not found.")

# exemplo de uso
# evaluator = PSNREvaluator()
# video1 = 'path/to/video1.mp4'
# video2 = 'path/to/video2.mp4'
# psnr_value = evaluator.evaluate(video1, video2)