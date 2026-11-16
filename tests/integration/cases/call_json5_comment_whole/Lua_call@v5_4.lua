local expected_events = {1, 42}
local event_index = 1
local function observe_event(actual)
    assert(event_index <= 2 and actual == expected_events[event_index])
    event_index = event_index + 1
end
local function f(a)
    observe_event(1); observe_event(a)
    return a + 100
end
local function verify_events() assert(event_index == 2 + 1) end
-- scalar heading
-- second heading line
-- scalar inline
-- inline continuation
-- scalar trailing
f(42)
verify_events()
