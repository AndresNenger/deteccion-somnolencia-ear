import pytest

from somnolencia.detector import (
    ESTADO_DESPIERTO,
    ESTADO_SIN_ROSTRO,
    ESTADO_SOMNOLIENTO,
    DrowsinessDetector,
    frames_from_seconds,
)


def test_ojos_abiertos_nunca_alertan():
    d = DrowsinessDetector(0.22, 15)
    for _ in range(100):
        s = d.update(0.30)
    assert not s.drowsy and s.counter == 0 and s.label == ESTADO_DESPIERTO


def test_alerta_solo_cuando_el_contador_supera_N():
    d = DrowsinessDetector(0.22, 15)
    estados = [d.update(0.10) for _ in range(16)]
    assert not any(s.drowsy for s in estados[:15])  # contador 1..15: aun no
    assert estados[15].drowsy and estados[15].label == ESTADO_SOMNOLIENTO  # contador 16 > 15


def test_un_parpadeo_corto_no_dispara_la_alerta():
    d = DrowsinessDetector(0.22, 15)
    for _ in range(5):
        d.update(0.10)
    s = d.update(0.30)
    assert s.counter == 0 and not s.drowsy


def test_umbral_es_estricto_ear_igual_al_umbral_es_ojo_abierto():
    d = DrowsinessDetector(0.22, 3)
    assert d.update(0.22).counter == 0


def test_recuperacion_tras_alerta():
    d = DrowsinessDetector(0.22, 3)
    for _ in range(10):
        d.update(0.05)
    s = d.update(0.30)
    assert not s.drowsy and s.counter == 0


def test_sin_rostro_reinicia_contador():
    d = DrowsinessDetector(0.22, 15)
    for _ in range(10):
        d.update(0.05)
    s = d.update(None)
    assert s.label == ESTADO_SIN_ROSTRO and s.ear is None and s.counter == 0 and not s.drowsy


def test_parametros_invalidos():
    with pytest.raises(ValueError):
        DrowsinessDetector(0.0, 15)
    with pytest.raises(ValueError):
        DrowsinessDetector(0.22, 0)


def test_frames_from_seconds():
    assert frames_from_seconds(0.5, 30) == 15
    assert frames_from_seconds(1.0, 15) == 15
    assert frames_from_seconds(0.001, 30) == 1
