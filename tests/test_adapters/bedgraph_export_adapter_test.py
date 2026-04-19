from types import SimpleNamespace

import DNA_analyser_IBP.adapters.cpg_adapter as cpg_adapter_module
import DNA_analyser_IBP.adapters.g4hunter_adapter as g4hunter_adapter_module
import DNA_analyser_IBP.adapters.rloopr_adapter as rloopr_adapter_module
import DNA_analyser_IBP.adapters.zdna_adapter as zdna_adapter_module
from DNA_analyser_IBP.adapters.cpg_adapter import CpGAdapter
from DNA_analyser_IBP.adapters.g4hunter_adapter import G4HunterAdapter
from DNA_analyser_IBP.adapters.rloopr_adapter import RLooprAdapter
from DNA_analyser_IBP.adapters.zdna_adapter import ZDnaAdapter
from DNA_analyser_IBP.models import User


def _user() -> User:
    user = User(email="test@test.cz", password="password", server="http://localhost")
    user.jwt = "jwt"
    return user


def test_g4hunter_export_csv_and_bedgraph(monkeypatch):
    calls = []

    def fake_get(url, headers, params):
        calls.append({"url": url, "headers": headers, "params": params})
        return SimpleNamespace(status_code=200, text="content")

    monkeypatch.setattr(g4hunter_adapter_module.requests, "get", fake_get)
    monkeypatch.setattr(
        g4hunter_adapter_module,
        "validate_text_response",
        lambda response, status_code: response.text,
    )

    adapter = G4HunterAdapter(user=_user())
    csv_content = adapter.export_csv(
        id="analyse-id", aggregate=False, base_start=12, base_end=44
    )
    bed_content = adapter.export_bedgraph(
        id="analyse-id", aggregate=False, base_start=12, base_end=44
    )

    assert csv_content == "content"
    assert bed_content == "content"
    assert calls[0]["url"].endswith("/analyse/g4hunter/analyse-id/quadruplex.csv")
    assert calls[1]["url"].endswith(
        "/analyse/g4hunter/analyse-id/quadruplex.bedgraph"
    )
    assert calls[0]["params"] == {
        "aggregate": "false",
        "base_start": 12,
        "base_end": 44,
    }
    assert calls[1]["params"] == {
        "aggregate": "false",
        "base_start": 12,
        "base_end": 44,
    }


def test_cpg_export_csv_and_bedgraph(monkeypatch):
    calls = []

    def fake_get(url, headers, params):
        calls.append({"url": url, "headers": headers, "params": params})
        return SimpleNamespace(status_code=200, text="content")

    monkeypatch.setattr(cpg_adapter_module.requests, "get", fake_get)
    monkeypatch.setattr(
        cpg_adapter_module,
        "validate_text_response",
        lambda response, status_code: response.text,
    )

    adapter = CpGAdapter(user=_user())
    csv_content = adapter.export_csv(id="analyse-id", base_start=1, base_end=2)
    bed_content = adapter.export_bedgraph(id="analyse-id", base_start=1, base_end=2)

    assert csv_content == "content"
    assert bed_content == "content"
    assert calls[0]["url"].endswith("/analyse/cpg/analyse-id/cpg.csv")
    assert calls[1]["url"].endswith("/analyse/cpg/analyse-id/cpg.bedgraph")
    assert calls[0]["params"] == {"base_start": 1, "base_end": 2}
    assert calls[1]["params"] == {"base_start": 1, "base_end": 2}


def test_rloopr_export_csv_and_bedgraph(monkeypatch):
    calls = []

    def fake_get(url, headers, params):
        calls.append({"url": url, "headers": headers, "params": params})
        return SimpleNamespace(status_code=200, text="content")

    monkeypatch.setattr(rloopr_adapter_module.requests, "get", fake_get)
    monkeypatch.setattr(
        rloopr_adapter_module,
        "validate_text_response",
        lambda response, status_code: response.text,
    )

    adapter = RLooprAdapter(user=_user())
    csv_content = adapter.export_csv(id="analyse-id", base_start=5, base_end=6)
    bed_content = adapter.export_bedgraph(id="analyse-id", base_start=5, base_end=6)

    assert csv_content == "content"
    assert bed_content == "content"
    assert calls[0]["url"].endswith("/analyse/rloopr/analyse-id/rloopr.csv")
    assert calls[1]["url"].endswith("/analyse/rloopr/analyse-id/rloopr.bedgraph")
    assert calls[0]["params"] == {"base_start": 5, "base_end": 6}
    assert calls[1]["params"] == {"base_start": 5, "base_end": 6}


def test_zdna_export_csv_and_bedgraph(monkeypatch):
    calls = []

    def fake_get(url, headers, params):
        calls.append({"url": url, "headers": headers, "params": params})
        return SimpleNamespace(status_code=200, text="content")

    monkeypatch.setattr(zdna_adapter_module.requests, "get", fake_get)
    monkeypatch.setattr(
        zdna_adapter_module,
        "validate_text_response",
        lambda response, status_code: response.text,
    )

    adapter = ZDnaAdapter(user=_user())
    csv_content = adapter.export_csv(id="analyse-id", base_start=7, base_end=8)
    bed_content = adapter.export_bedgraph(id="analyse-id", base_start=7, base_end=8)

    assert csv_content == "content"
    assert bed_content == "content"
    assert calls[0]["url"].endswith("/analyse/zdna/analyse-id/zdna.csv")
    assert calls[1]["url"].endswith("/analyse/zdna/analyse-id/zdna.bedgraph")
    assert calls[0]["params"] == {"base_start": 7, "base_end": 8}
    assert calls[1]["params"] == {"base_start": 7, "base_end": 8}
