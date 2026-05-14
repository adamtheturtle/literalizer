local app = { client: { fetch(payload):: null } };
local emit(_arg) = null;
[
    emit(app.client.fetch(payload="hello")),
    emit(app.client.fetch(payload=42)),
    emit(app.client.fetch(payload=true)),
]
