local expected_events = {1, 42, 1, 42, 1, 142}
local event_index = 1
local function observe_event(actual)
    assert(event_index <= 6 and actual == expected_events[event_index])
    event_index = event_index + 1
end
local function make_widget(count)
    observe_event(1); observe_event(count)
    return count + 100
end
local function verify_events() assert(event_index == 6 + 1) end
local my_data = 42
make_widget(my_data)
my_data = make_widget(my_data)
make_widget(my_data)
verify_events()
