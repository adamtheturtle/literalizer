local app = { process: { fetch(data):: null } };
[
    app.process.fetch(data={data: "hello"}),
    app.process.fetch(data={data: 42}),
    app.process.fetch(data={data: true}),
]
