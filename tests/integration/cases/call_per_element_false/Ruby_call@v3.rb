$event_index = 0
def observe_event(actual)
  expected = [1, 1]
  raise "receiver event changed" unless $event_index < 2 && actual == expected[$event_index]
  $event_index += 1
end
def process(data:)
  observe_event(1); observe_event(data)
  data + 100
end
def verify_events
  raise "missing receiver events" unless $event_index == 2
end
process(data: 1)
verify_events()
