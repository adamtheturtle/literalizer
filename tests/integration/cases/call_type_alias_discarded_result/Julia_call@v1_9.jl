event_index = Ref(1)
function observe_event(actual::Integer)
    expected = [1, 1]
    @assert event_index[] <= 2 && actual == expected[event_index[]]
    event_index[] += 1
end
function process(; value)
    observe_event(1); observe_event(value)
    value + 100
end
function verify_events()
    @assert event_index[] == 2 + 1
end
process(value=1)
verify_events()
