"""Exercise linkcheck recovery against a real local HTTP server."""

import subprocess
import sys
import threading
from pathlib import Path
from wsgiref.simple_server import make_server
from wsgiref.types import StartResponse, WSGIEnvironment

import pytest


@pytest.mark.parametrize(
    argnames=(
        "first_status",
        "second_status",
        "warning",
        "exit_status",
        "request_count",
    ),
    argvalues=[
        (200, 200, "", 0, 1),
        (504, 200, "", 0, 3),
        (502, 200, "", 0, 3),
        (504, 504, "", 1, 4),
        (404, 200, "", 1, 2),
        (504, 200, ".. unknown-directive::\n", 1, 2),
    ],
)
def test_linkcheck_recovery(
    tmp_path: Path,
    *,
    first_status: int,
    second_status: int,
    warning: str,
    exit_status: int,
    request_count: int,
) -> None:
    """Retry server errors once while preserving broken links and warnings."""
    requested: list[str] = []
    initial_requests = 2

    def application(
        environ: WSGIEnvironment, start_response: StartResponse
    ) -> list[bytes]:
        """Serve a link that optionally recovers after the first build."""
        requested.append(environ["REQUEST_METHOD"])
        status = (
            first_status
            if len(requested) <= initial_requests
            else second_status
        )
        _ = start_response(f"{status} test", [])
        return []

    source = tmp_path / "source"
    source.mkdir()
    _ = (source / "conf.py").write_text(
        data="linkcheck_retries = 1\n", encoding="utf-8"
    )
    with make_server(host="127.0.0.1", port=0, app=application) as server:
        thread = threading.Thread(target=server.serve_forever, daemon=True)
        thread.start()
        host = "127.0.0.1"
        port = server.server_port
        _ = (source / "index.rst").write_text(
            data=f"Links\n=====\n\nhttp://{host}:{port}/link\n\n{warning}",
            encoding="utf-8",
        )
        try:
            result = subprocess.run(
                args=[
                    sys.executable,
                    "-m",
                    "scripts.check_documentation_links",
                    str(object=source),
                    str(object=tmp_path / "build"),
                    str(object=tmp_path / "doctrees"),
                    "--retry-delay",
                    "0.1",
                ],
                capture_output=True,
                text=True,
                check=False,
                timeout=30,
            )
        finally:
            server.shutdown()
            thread.join()
    assert result.returncode == exit_status, result.stdout + result.stderr
    assert len(requested) == request_count
    assert ("Retrying linkcheck" in result.stderr) == (
        request_count > initial_requests
    )
