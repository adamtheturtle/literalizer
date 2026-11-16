$event_index = 0
def observe_event(actual)
  expected = [1, 1]
  raise "receiver event changed" unless $event_index < 2 && actual == expected[$event_index]
  $event_index += 1
end
def process(value:)
  observe_event(1); observe_event(value)
  value + 100
end
def verify_events
  raise "missing receiver events" unless $event_index == 2
end
value = 1
process(value: value)
verify_events()
