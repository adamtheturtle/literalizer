$event_index = 0
def observe_event(actual)
  expected = [2, 0, 1, 1, 2, 101]
  raise "receiver event changed" unless $event_index < 6 && actual == expected[$event_index]
  $event_index += 1
end
def make_widget(count:)
  observe_event(1); observe_event(count)
  count + 100
end
def consume_widget(count:)
  observe_event(2); observe_event(count)
end
def verify_events
  raise "missing receiver events" unless $event_index == 6
end
my_data = 0
consume_widget(count: my_data)
my_data = make_widget(count: 1)
consume_widget(count: my_data)
verify_events()
