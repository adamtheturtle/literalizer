local expected_events = {1, 42, 2, 142}
local event_index = 1
local function observe_event(actual)
    assert(event_index <= 4 and actual == expected_events[event_index])
    event_index = event_index + 1
end
local function make_widget(value)
    observe_event(1); observe_event(value)
    return value + 100
end
local function consume(value) observe_event(2); observe_event(value) end
local function verify_events() assert(event_index == 4 + 1) end
local my_data = make_widget(42)
consume(my_data)
verify_events()
