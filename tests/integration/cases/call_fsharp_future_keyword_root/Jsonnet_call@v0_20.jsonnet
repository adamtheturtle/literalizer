local process = { api: { fetch(data):: null } };
[
    process.api.fetch(data={data: "hello"}),
    process.api.fetch(data={data: 42}),
    process.api.fetch(data={data: true}),
]
