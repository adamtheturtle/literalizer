"""Exercise artifact recovery and integrity with real HTTP downloads."""

import hashlib
import shutil
import subprocess
import threading
from pathlib import Path
from wsgiref.simple_server import make_server
from wsgiref.types import StartResponse, WSGIEnvironment

import pytest


@pytest.mark.skipif(
    shutil.which(cmd="bash") is None or shutil.which(cmd="shasum") is None,
    reason="artifact setup requires Bash and shasum",
)
@pytest.mark.parametrize(
    argnames=("first_status", "second_status", "body", "exit_status", "paths"),
    argvalues=[
        (200, 200, b"artifact", 0, ["/first"]),
        (404, 200, b"artifact", 0, ["/first"] * 3 + ["/second"]),
        (200, 200, b"corrupt", 1, ["/first"]),
        (404, 404, b"artifact", 1, ["/first"] * 3 + ["/second"] * 3),
    ],
)
def test_checked_download(
    tmp_path: Path,
    *,
    first_status: int,
    second_status: int,
    body: bytes,
    exit_status: int,
    paths: list[str],
) -> None:
    """Recover HTTP failures, reject corruption, and preserve existing
    files.
    """
    requested: list[str] = []
    bash_path = shutil.which(cmd="bash")
    assert bash_path is not None
    statuses = {"/first": first_status, "/second": second_status}

    def application(
        environ: WSGIEnvironment, start_response: StartResponse
    ) -> list[bytes]:
        """Serve the selected artifact or HTTP error."""
        path = environ["PATH_INFO"]
        requested.append(path)
        _ = start_response(f"{statuses[path]} test", [])
        return [body]

    destination = tmp_path / "download with spaces.jar"
    _ = destination.write_bytes(data=b"previous")
    with make_server(host="127.0.0.1", port=0, app=application) as server:
        thread = threading.Thread(target=server.serve_forever, daemon=True)
        thread.start()
        host = "127.0.0.1"
        port = server.server_port
        try:
            result = subprocess.run(
                args=[
                    bash_path,
                    "scripts/download-checked.sh",
                    hashlib.sha256(string=b"artifact").hexdigest(),
                    str(object=destination),
                    f"http://{host}:{port}/first",
                    f"http://{host}:{port}/second",
                ],
                capture_output=True,
                text=True,
                check=False,
                timeout=30,
            )
        finally:
            server.shutdown()
            thread.join()
    assert result.returncode == exit_status, result.stderr
    assert requested == paths
    expected = b"artifact" if exit_status == 0 else b"previous"
    assert destination.read_bytes() == expected
    assert list(tmp_path.iterdir()) == [destination]
