def expectedEvents = [1, 1, 2, 101, 3, 41, 1, 2, 2, 102, 3, 42]
def eventIndex = [0]
def observeEvent = { long actual ->
    assert eventIndex[0] < 12 && actual == expectedEvents[eventIndex[0]]
    eventIndex[0]++
}
def process = { Map args -> def value = args.value; observeEvent(1); observeEvent(value); value + 100 }
def emit = { long actual, long zipped -> observeEvent(2); observeEvent(actual); observeEvent(3); observeEvent(zipped) }
def verify_events = { -> assert eventIndex[0] == 12 }
emit(process(value: 1), 41)
emit(process(value: 2), 42)
verify_events()
