$event_index = 0
def observe_event(actual)
  expected = [1, 1, 2, 101, 3, 42]
  raise "receiver event changed" unless $event_index < 6 && actual == expected[$event_index]
  $event_index += 1
end
def process(value:)
  observe_event(1); observe_event(value)
  value + 100
end
def emit(actual, zipped)
  observe_event(2); observe_event(actual)
  observe_event(3); observe_event(zipped)
end
def verify_events
  raise "missing receiver events" unless $event_index == 6
end
emit(process(value: 1), 42)
verify_events()
