local app = { client: { fetch(payload):: null } };
[
    app.client.fetch(payload="hello"),
    app.client.fetch(payload=42),
    app.client.fetch(payload=true),
]
