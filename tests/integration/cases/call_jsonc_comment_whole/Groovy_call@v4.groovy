def expectedEvents = [1, 42]
def eventIndex = [0]
def observeEvent = { long actual ->
    assert eventIndex[0] < 2 && actual == expectedEvents[eventIndex[0]]
    eventIndex[0]++
}
def f = { Map args -> def value = args.a; observeEvent(1); observeEvent(value); value + 100 }
def verify_events = { -> assert eventIndex[0] == 2 }
// scalar heading
// second heading line
// scalar inline
// inline continuation
// scalar trailing
f(a: 42)
verify_events()
