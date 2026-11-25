def expectedEvents = [1, 42, 2, 142]
def eventIndex = [0]
def observeEvent = { long actual ->
    assert eventIndex[0] < 4 && actual == expectedEvents[eventIndex[0]]
    eventIndex[0]++
}
def process = { Map args -> def value = args.value; observeEvent(1); observeEvent(value); value + 100 }
def emit = { long actual -> observeEvent(2); observeEvent(actual) }
def verify_events = { -> assert eventIndex[0] == 4 }
emit(process(value: 42))
verify_events()
