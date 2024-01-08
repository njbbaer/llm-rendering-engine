import json
import yaml
import pytest

from src.render_chat import render_chat


@pytest.fixture
def template_str():
    with open("src/chat_template.yml", "r") as file:
        return file.read()


@pytest.fixture
def source_yaml():
    with open("tests/source.yml", "r") as file:
        return yaml.safe_load(file)


@pytest.fixture
def target_json():
    with open("tests/target.json", "r") as file:
        return json.load(file)


def test_render_chat(template_str, source_yaml, target_json):
    result = render_chat(template_str, source_yaml)
    assert result == target_json
