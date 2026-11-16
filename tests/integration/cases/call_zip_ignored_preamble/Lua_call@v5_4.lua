local expected_events = {1, 1, 1, 2}
local event_index = 1
local function observe_event(actual)
    assert(event_index <= 4 and actual == expected_events[event_index])
    event_index = event_index + 1
end
local function process(value)
    observe_event(1); observe_event(value)
    return value + 100
end
local function verify_events() assert(event_index == 4 + 1) end
process(1)
process(2)
verify_events()
