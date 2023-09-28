from utils.utils import get_data, last_operations, format_operation
import pytest
import os


@pytest.fixture(autouse=True)
def set_working_directory():
    project_directory = os.path.abspath(os.path.dirname(__file__))
    os.chdir(project_directory)


def test_get_data():
    assert len(get_data()) > 0


def test_get_data_file_not_found():
    with pytest.raises(FileNotFoundError):
        get_data(path="test")


def test_last_operations():
    assert len(last_operations()) > 0
