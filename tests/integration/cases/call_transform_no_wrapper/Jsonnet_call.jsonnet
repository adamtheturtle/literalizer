local client = { api: { request(data):: null } };
[
    client.api.request(data="hello"),
    client.api.request(data=42),
    client.api.request(data=true),
]
