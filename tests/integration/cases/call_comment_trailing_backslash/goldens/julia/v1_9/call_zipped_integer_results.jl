event_index = Ref(1)
function observe_event(actual::Integer)
    expected = [1, 1, 2, 101, 3, 41, 1, 2, 2, 102, 3, 42]
    @assert event_index[] <= 12 && actual == expected[event_index[]]
    event_index[] += 1
end
function process(; value)
    observe_event(1); observe_event(value)
    value + 100
end
function emit(actual, zipped)
    observe_event(2); observe_event(actual)
    observe_event(3); observe_event(zipped)
end
function verify_events()
    @assert event_index[] == 12 + 1
end
emit(process(value=1), 41)
emit(process(value=2), 42)
verify_events()
