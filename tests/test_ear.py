import numpy as np
import pytest

from somnolencia.ear import LEFT_EYE, RIGHT_EYE, eye_aspect_ratio, landmarks_to_pixels, mean_ear


def make_eye(opening: float, width: float = 30.0) -> np.ndarray:
    """Ojo sintetico: p1/p4 en las comisuras y pares p2-p6, p3-p5 separados `opening`."""
    h = opening / 2
    return np.array(
        [[0, 0], [width * 0.33, -h], [width * 0.66, -h], [width, 0], [width * 0.66, h], [width * 0.33, h]]
    )


def test_ear_ojo_abierto_valor_conocido():
    # a = b = 10, c = 30  ->  EAR = 20 / 60
    assert eye_aspect_ratio(make_eye(10.0)) == pytest.approx(1 / 3)


def test_ear_ojo_cerrado_es_cero():
    assert eye_aspect_ratio(make_eye(0.0)) == pytest.approx(0.0)


def test_ear_invariante_a_la_escala():
    assert eye_aspect_ratio(make_eye(6.0) * 5) == pytest.approx(eye_aspect_ratio(make_eye(6.0)))


def test_ear_monotono_con_la_apertura():
    assert eye_aspect_ratio(make_eye(4.0)) < eye_aspect_ratio(make_eye(8.0))


def test_ear_forma_invalida():
    with pytest.raises(ValueError):
        eye_aspect_ratio(np.zeros((5, 2)))


def test_ear_comisuras_coincidentes_no_divide_por_cero():
    assert eye_aspect_ratio(np.zeros((6, 2))) == 0.0


def test_mean_ear_promedia_ambos_ojos():
    lm = np.zeros((478, 2))
    lm[LEFT_EYE] = make_eye(10.0)
    lm[RIGHT_EYE] = make_eye(4.0)
    avg, left, right = mean_ear(lm)
    assert left == pytest.approx(1 / 3)
    assert right == pytest.approx(4 / 30)
    assert avg == pytest.approx((left + right) / 2)


def test_landmarks_to_pixels_escala_por_ancho_y_alto():
    px = landmarks_to_pixels(np.array([[0.5, 0.5], [1.0, 0.0]]), 640, 480)
    assert px.tolist() == [[320.0, 240.0], [640.0, 0.0]]


def test_indices_de_ojos_son_6_y_distintos():
    assert len(LEFT_EYE) == len(RIGHT_EYE) == 6
    assert not set(LEFT_EYE) & set(RIGHT_EYE)
