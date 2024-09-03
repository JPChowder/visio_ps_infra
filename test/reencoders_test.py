import pytest
from unittest.mock import patch
from pathlib import Path

from reencoder import VP8Reencoder, VP9Reencoder, AV1Reencoder


@pytest.fixture
def vp8_reencoder():
    return VP8Reencoder("input.mp4", "output.webm", crf=30, speed=4, threads=2)

@pytest.fixture
def vp9_reencoder():
    return VP9Reencoder("input.mp4", "output.webm", crf=30, speed=4, threads=2)

@pytest.fixture
def av1_reencoder():
    return AV1Reencoder("input.mp4", "output.mkv", crf=30, speed=8, threads=2, bitrate="1M")

@patch('subprocess.run')
def test_vp8_reencode(mock_subprocess_run, vp8_reencoder):
    vp8_reencoder.reencode()
    mock_subprocess_run.assert_called_once_with([
        'ffmpeg', '-i', 'input.mp4',
        '-c:v', 'libvpx',
        '-crf', '30',
        '-speed', '4',
        '-threads', '2',
        'output.webm'
    ], check=True)

@patch('subprocess.run')
def test_vp9_reencode(mock_subprocess_run, vp9_reencoder):
    vp9_reencoder.reencode()
    mock_subprocess_run.assert_called_once_with([
        'ffmpeg', '-i', 'input.mp4',
        '-c:v', 'libvpx-vp9',
        '-crf', '30',
        '-speed', '4',
        '-threads', '2',
        'output.webm'
    ], check=True)

@patch('subprocess.run')
def test_av1_reencode(mock_subprocess_run, av1_reencoder):
    av1_reencoder.reencode()
    mock_subprocess_run.assert_called_once_with([
        'ffmpeg', '-i', 'input.mp4',
        '-c:v', 'libaom-av1',
        '-crf', '30',
        '-preset', '8',
        '-threads', '2',
        '-b:v', '1M',
        'output.mkv'
    ], check=True)

# Uma vez que eh usado o decorator @patch para o comando subprocess.run
# estes testes estao aferindo se a chamada correta para ffmpeg eh feita
# pelos metodos da classe VideoReencoder