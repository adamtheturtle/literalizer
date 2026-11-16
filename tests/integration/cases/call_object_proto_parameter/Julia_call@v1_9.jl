event_index = Ref(1)
function observe_event(actual::Integer)
    expected = [1, 1]
    @assert event_index[] <= 2 && actual == expected[event_index[]]
    event_index[] += 1
end
function capture(; __proto__)
    observe_event(1); observe_event(__proto__)
    __proto__ + 100
end
function verify_events()
    @assert event_index[] == 2 + 1
end
capture(__proto__=1)
verify_events()
