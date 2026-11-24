def expectedEvents = [1, 1]
def eventIndex = [0]
def observeEvent = { long actual ->
    assert eventIndex[0] < 2 && actual == expectedEvents[eventIndex[0]]
    eventIndex[0]++
}
def process = { Map args -> def value = args.data; observeEvent(1); observeEvent(value); value + 100 }
def verify_events = { -> assert eventIndex[0] == 2 }
process(data: 1)
verify_events()
