local expected_events = {1, 1, 2, 101, 3, 41, 1, 2, 2, 102, 3, 42}
local event_index = 1
local function observe_event(actual)
    assert(event_index <= 12 and actual == expected_events[event_index])
    event_index = event_index + 1
end
local function process(value)
    observe_event(1); observe_event(value)
    return value + 100
end
local function emit(actual, zipped) observe_event(2); observe_event(actual) observe_event(3); observe_event(zipped) end
local function verify_events() assert(event_index == 12 + 1) end
emit(process(1), 41)
emit(process(2), 42)
verify_events()
