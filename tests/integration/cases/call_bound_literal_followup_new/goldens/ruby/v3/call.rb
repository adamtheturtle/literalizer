$event_index = 0
def observe_event(actual)
  expected = [1, 42, 2, 142]
  raise "receiver event changed" unless $event_index < 4 && actual == expected[$event_index]
  $event_index += 1
end
def make_widget(value:)
  observe_event(1); observe_event(value)
  value + 100
end
def consume(value:)
  observe_event(2); observe_event(value)
end
def verify_events
  raise "missing receiver events" unless $event_index == 4
end
my_data = make_widget(value: 42)
consume(value: my_data)
verify_events()
