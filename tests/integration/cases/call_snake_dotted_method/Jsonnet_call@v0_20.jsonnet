local my_app = { http_client: { fetch(payload):: null } };
[
    my_app.http_client.fetch(payload="hello"),
    my_app.http_client.fetch(payload=42),
    my_app.http_client.fetch(payload=true),
]
