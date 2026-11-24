def expectedEvents = [1, -1, 1, -2, 1, -3]
def eventIndex = [0]
def observeEvent = { long actual ->
    assert eventIndex[0] < 6 && actual == expectedEvents[eventIndex[0]]
    eventIndex[0]++
}
def process = { Map args -> def value = args.value; observeEvent(1); observeEvent(value); value + 100 }
def verify_events = { -> assert eventIndex[0] == 6 }
process(value: -1)
process(value: -2)
process(value: -3)
verify_events()
