def expectedEvents = [1, 42, 2, 142]
def eventIndex = [0]
def observeEvent = { long actual ->
    assert eventIndex[0] < 4 && actual == expectedEvents[eventIndex[0]]
    eventIndex[0]++
}
def make_widget = { Map args -> def value = args.value; observeEvent(1); observeEvent(value); value + 100 }
def consume = { Map args -> observeEvent(2); observeEvent(args.value) }
def verify_events = { -> assert eventIndex[0] == 4 }
def my_data = make_widget(value: 42)
consume(value: my_data)
verify_events()
