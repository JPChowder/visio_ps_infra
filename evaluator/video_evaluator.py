from abc import ABC, abstractmethod
import subprocess

class VideoEvaluator(ABC):
    
    @abstractmethod
    def evaluate(self, video1_path: str, video2_path: str) -> float:
        """
        Avalia a qualidade comparativa entre um video original e um convertido.
        
        Args:
            video1_path (str): Caminho para o video original.
            video2_path (str): Caminho para o video convertido.
        
        Returns:
            float: A metrica de qualidade relativa entre os videos.
        """
        pass