event_index = Ref(1)
function observe_event(actual::Integer)
    expected = [1, 1]
    @assert event_index[] <= 2 && actual == expected[event_index[]]
    event_index[] += 1
end
function process(; data)
    observe_event(1); observe_event(data)
    data + 100
end
function verify_events()
    @assert event_index[] == 2 + 1
end
process(data=1)
verify_events()
