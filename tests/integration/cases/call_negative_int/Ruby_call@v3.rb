$event_index = 0
def observe_event(actual)
  expected = [1, -1, 1, -2, 1, -3]
  raise "receiver event changed" unless $event_index < 6 && actual == expected[$event_index]
  $event_index += 1
end
def process(value:)
  observe_event(1); observe_event(value)
  value + 100
end
def verify_events
  raise "missing receiver events" unless $event_index == 6
end
process(value: -1)
process(value: -2)
process(value: -3)
verify_events()
