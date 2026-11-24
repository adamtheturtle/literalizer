event_index = Ref(1)
function observe_event(actual::Integer)
    expected = [1, 1, 1, 2]
    @assert event_index[] <= 4 && actual == expected[event_index[]]
    event_index[] += 1
end
function process(; value)
    observe_event(1); observe_event(value)
    value + 100
end
function verify_events()
    @assert event_index[] == 4 + 1
end
process(value=1)  # trail \ .
process(value=2)  # second
verify_events()
