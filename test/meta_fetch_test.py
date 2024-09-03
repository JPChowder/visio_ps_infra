import pytest
import subprocess
import json
import os
from unittest.mock import patch

from utils.meta_fetch import MetaFetch

mock_ffprobe_output = json.dumps({
    "streams": [
        {
            "bit_rate": "388015",
            "duration": "19.99",
            "r_frame_rate": "25/1",
            "codec_name": "h264"
        }
    ]
})

# para o bom funcionamento deste teste eh necessario que o
# video que servira para os testes tenha sido baixado
@pytest.fixture
def metafetch():
    return MetaFetch("videos_visio/h264.mp4")

@patch('subprocess.run')
@patch('os.path.getsize')
def test_get_video_info(mock_getsize, mock_subprocess_run, metafetch):
    mock_subprocess_run.return_value.stdout = mock_ffprobe_output.encode('utf-8')
    mock_subprocess_run.return_value.stderr = b""
    
    info = metafetch.get_video_info()
    
    assert info['streams'][0]['bit_rate'] == "388015"
    assert info['streams'][0]['duration'] == "19.99"
    assert info['streams'][0]['r_frame_rate'] == "25/1"
    assert info['streams'][0]['codec_name'] == "h264"

@patch('subprocess.run')
@patch('os.path.getsize')
def test_get_bitrate(mock_getsize, mock_subprocess_run, metafetch):
    mock_subprocess_run.return_value.stdout = mock_ffprobe_output.encode('utf-8')
    mock_subprocess_run.return_value.stderr = b""
    
    bitrate = metafetch.get_bitrate()
    assert bitrate == "388015"

@patch('subprocess.run')
@patch('os.path.getsize')
def test_get_duration(mock_getsize, mock_subprocess_run, metafetch):
    mock_subprocess_run.return_value.stdout = mock_ffprobe_output.encode('utf-8')
    mock_subprocess_run.return_value.stderr = b""
    
    duration = metafetch.get_duration()
    assert duration == 19.99

@patch('subprocess.run')
@patch('os.path.getsize')
def test_get_frame_rate(mock_getsize, mock_subprocess_run, metafetch):
    mock_subprocess_run.return_value.stdout = mock_ffprobe_output.encode('utf-8')
    mock_subprocess_run.return_value.stderr = b""
    
    frame_rate = metafetch.get_frame_rate()
    assert frame_rate == 25.0

@patch('subprocess.run')
@patch('os.path.getsize')
def test_get_encoding(mock_getsize, mock_subprocess_run, metafetch):
    mock_subprocess_run.return_value.stdout = mock_ffprobe_output.encode('utf-8')
    mock_subprocess_run.return_value.stderr = b""
    
    encoding = metafetch.get_encoding()
    assert encoding == "h264"

@patch('subprocess.run')
@patch('os.path.getsize')
def test_get_size(mock_getsize, mock_subprocess_run, metafetch):
    mock_getsize.return_value = 388015
    
    size = metafetch.get_size()
    assert size == 388015

# Nesta bateria de testes os decorators @patch sao usados para que
# nos metodos de MetaFetch nao sejam rodados os comandos 
# subprocess.run e os.path.getsize, apenas eh aferido se a chamada
# correta esta sendo feito.