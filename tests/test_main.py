import pytest

from project_name.main import func


def test_func():   
    assert func(3,4) == 7
    assert func(3.5,4.5) == 8.0
    assert func('welcome',' back') == 'welcome back'
    
