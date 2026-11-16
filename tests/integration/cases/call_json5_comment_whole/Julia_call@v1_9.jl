event_index = Ref(1)
function observe_event(actual::Integer)
    expected = [1, 42]
    @assert event_index[] <= 2 && actual == expected[event_index[]]
    event_index[] += 1
end
function f(; a)
    observe_event(1); observe_event(a)
    a + 100
end
function verify_events()
    @assert event_index[] == 2 + 1
end
# scalar heading
# second heading line
# scalar inline
# inline continuation
# scalar trailing
f(a=42)
verify_events()
