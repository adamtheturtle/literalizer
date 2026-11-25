def expectedEvents = [2, 0, 1, 1, 2, 101]
def eventIndex = [0]
def observeEvent = { long actual ->
    assert eventIndex[0] < 6 && actual == expectedEvents[eventIndex[0]]
    eventIndex[0]++
}
def make_widget = { Map args -> def value = args.count; observeEvent(1); observeEvent(value); value + 100 }
def consume_widget = { Map args -> observeEvent(2); observeEvent(args.count) }
def verify_events = { -> assert eventIndex[0] == 6 }
def my_data = 0
consume_widget(count: my_data)
my_data = make_widget(count: 1)
consume_widget(count: my_data)
verify_events()
