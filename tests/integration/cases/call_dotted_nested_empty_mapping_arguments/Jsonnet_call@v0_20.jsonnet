local api = { worker: { process(values, count):: null } };
[
    api.worker.process(values=[1, {}], count=42),
    api.worker.process(values=[2, {x: "s"}], count=43),
]
