from google.cloud import storage
import os

class VideoDownloader:
    def __init__(self):
        # Como nao usaremos chave de acesso faremos uso de um cliente anonimo
        self.client = storage.Client.create_anonymous_client()
    
    def download_video(self, gcs_path, destination_folder):
        """
        Realiza o download de videos de um bucket GCS.

        Args:
            gcs_path: Link para o video salvo em um bucket GCS.
            destination_folder: Pasta de destino para o video baixado.

        Returns:
            destination_path: retorna o caminho para o video baixado
        """
        # Separacao do nome do bucket e do video a partir do link
        bucket_name, blob_name = self.parse_gcs_path(gcs_path)
        bucket = self.client.bucket(bucket_name)
        blob = bucket.blob(blob_name)
        
        # Determinar o caminho em que o arquivo sera salvo
        destination_path = os.path.join(destination_folder, os.path.basename(blob_name))
        
        # Download
        blob.download_to_filename(destination_path)
        print(f"Video downloaded to {destination_path}")

        return destination_path

    def parse_gcs_path(self, gcs_path):
        # limpando o nome
        path = gcs_path.replace("gs://", "")
        bucket_name, blob_name = path.split("/", 1)
        return bucket_name, blob_name

# Uso
# downloader = VideoDownloader()
# downloader.download_video("gs://video_samples/video.mp4", "./downloads")