$event_index = 0
def observe_event(actual)
  expected = [2, 42, 1, 42, 2, 142]
  raise "receiver event changed" unless $event_index < 6 && actual == expected[$event_index]
  $event_index += 1
end
def make_widget(count:)
  observe_event(1); observe_event(count)
  count + 100
end
def consume(count:)
  observe_event(2); observe_event(count)
end
def verify_events
  raise "missing receiver events" unless $event_index == 6
end
my_data = 42
consume(count: my_data)
my_data = make_widget(count: 42)
consume(count: my_data)
verify_events()
