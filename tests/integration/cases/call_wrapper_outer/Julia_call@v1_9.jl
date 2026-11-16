event_index = Ref(1)
function observe_event(actual::Integer)
    expected = [1, 42, 2, 142]
    @assert event_index[] <= 4 && actual == expected[event_index[]]
    event_index[] += 1
end
function process(; value)
    observe_event(1); observe_event(value)
    value + 100
end
function emit(actual)
    observe_event(2); observe_event(actual)
end
function verify_events()
    @assert event_index[] == 4 + 1
end
emit(process(value=42))
verify_events()
