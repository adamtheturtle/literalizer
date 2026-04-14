local obj = { api: { client: { post(data):: null } } };
[
    obj.api.client.post(data="hello"),
    obj.api.client.post(data=42),
    obj.api.client.post(data=true),
]
