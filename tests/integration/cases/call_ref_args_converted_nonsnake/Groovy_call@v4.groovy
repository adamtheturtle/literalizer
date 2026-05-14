def process(Map _args) { null }
def myVar = [
    1,
    2,
    3,
]
def myOther = [
    4,
    5,
    6,
]
process(data: myVar, count: 42)
process(data: myOther, count: 7)
