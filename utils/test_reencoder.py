import os
import time
import subprocess
import pandas as pd
from evaluator import PSNREvaluator
from utils.meta_fetch import MetaFetch

def test_reencoder(reencoder, input_video):
    output_video = reencoder.output_file

    # Medida de tempo entre o começo e o fim do reencoding
    start_time = time.time()
    reencoder.reencode()
    elapsed_time = time.time() - start_time

    # Criacao da classe de avaliacao do video resultante
    evaluator = PSNREvaluator()
    evaluation_result = evaluator.evaluate(input_video, output_video)

    # Coleta informacoes dos videos usando o utilitario MetaFetch
    video_info = MetaFetch(output_video)
    output_codec = video_info.get_encoding()
    output_size = video_info.get_size()

    video_info = MetaFetch(input_video)
    input_size = video_info.get_size()

    # Coleta as opcoes usadas no reencoding
    options = {
        "crf": reencoder.crf,
        "speed": reencoder.speed,
        "bitrate": reencoder.bitrate,
        "threads": reencoder.threads
    }

    return {
        "codec": output_codec,
        "options": options,
        "input_size": input_size,
        "output_size": output_size,
        "evaluation_result": evaluation_result,
        "elapsed_time": elapsed_time
    }

def run_tests_and_save_results(reencoder_class, input_video, output_template, crf_values, speed_values, threads=2, bitrate=None):
    results = []

    # Loop sobre as combinacoes de crf e speed
    for crf in crf_values:
        for speed in speed_values:
            output_video = output_template.format(crf=crf, speed=speed)
            reencoder = reencoder_class(input_video, output_video, crf=crf, speed=speed, threads=threads, bitrate=bitrate)

            result = test_reencoder(reencoder, input_video)

            # Adiciona crf e speed ao dicionario de resultados
            result['crf'] = crf
            result['speed'] = speed
            result['bitrate'] = bitrate

            # Soma os resultados ao final do dicionario
            results.append(result)

    # Conversao em DataFrame antes do retorno
    df = pd.DataFrame(results)
    return df

# Exemplo de uso
# input_video = "video.vid"
# output_template = "voutput_encod-in_encod-out_crf{crf}_speed{speed}.vid"
# crf_values = [15, 30, 50]
# speed_values = [2, 4]
# threads = 2
# input_video_info = MetaFetch(input_video)
# bitrate = input_video_info.get_bitrate()
# df_results_1 = run_tests_and_save_results(ReencoderClass, input_video, output_template, crf_values, speed_values, threads, bitrate)