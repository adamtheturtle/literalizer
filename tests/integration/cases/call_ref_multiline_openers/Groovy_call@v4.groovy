def consume(Map _args) { null }
def foo = 42
consume(items: [
    [
        "other": 1,
    ],
    foo,
], mapping: [
    "left": foo,
    "other": 1,
])
