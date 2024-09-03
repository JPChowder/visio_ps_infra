import pytest
from unittest.mock import patch

from evaluator import PSNREvaluator


mock_ffmpeg_stderr_output = b"""
Stream #0:0: Video: vp9, yuv420p(progressive), 2048x1536 [SAR 1:1 DAR 4:3], q=2-31, 200 kb/s, 15 fps, 15 tbn
    Metadata:
        encoder         : Lavf61.5.101
[Parsed_psnr_1 @ 0x123456] PSNR y:24.940925 u:23.938192 v:23.641771 average:24.138969 min:23.298059 max:26.880485
[out#0/null @ 0x56238d949040] video:774KiB audio:0KiB subtitle:0KiB other streams:0KiB global headers:0KiB muxing overhead: unknown
frame=  969 fps=5.6 q=30.0 Lsize=    4864KiB time=00:01:04.80 bitrate= 614.9kbits/s speed=0.377x
"""

class MockPopen:
    def __init__(self, *args, **kwargs):
        self.stdout = b""
        self.stderr = mock_ffmpeg_stderr_output

    def communicate(self):
        return self.stdout, self.stderr

@pytest.fixture
def psnr_evaluator():
    return PSNREvaluator()

@patch('subprocess.Popen', new=MockPopen)
def test_psnr_evaluate(psnr_evaluator):
    psnr_value = psnr_evaluator.evaluate("video1.mp4", "video2.mp4")
    assert psnr_value == 24.138969

@patch('subprocess.Popen', new=MockPopen)
def test_psnr_evaluate_no_average(psnr_evaluator):
    class MockPopenNoAverage:
        def __init__(self, *args, **kwargs):
            self.stdout = b""
            self.stderr = b"""
Stream #0:0: Video: vp9, yuv420p(progressive), 2048x1536 [SAR 1:1 DAR 4:3], q=2-31, 200 kb/s, 15 fps, 15 tbn
    Metadata:
        encoder         : Lavf61.5.101
[Parsed_psnr_1 @ 0x123456] PSNR y:24.940925 u:23.938192 v:23.641771 min:23.298059 max:26.880485
[out#0/null @ 0x56238d949040] video:774KiB audio:0KiB subtitle:0KiB other streams:0KiB global headers:0KiB muxing overhead: unknown
frame=  969 fps=5.6 q=30.0 Lsize=    4864KiB time=00:01:04.80 bitrate= 614.9kbits/s speed=0.377x
            """

        def communicate(self):
            return self.stdout, self.stderr

    with patch('subprocess.Popen', new=MockPopenNoAverage):
        with pytest.raises(ValueError, match="PSNR calculation failed: 'average' value not found."):
            psnr_evaluator.evaluate("video1.mp4", "video2.mp4")

# Este conjunto de testes usa o decorator @patch e as classes MockPopen 
# e MockPopenNoAverage para simular o comportamento da chamada de
# subprocess.Popen, o uso das classes se faz necessario para se popular
# os campos stdout e stderr usados pelo avaliador original. 