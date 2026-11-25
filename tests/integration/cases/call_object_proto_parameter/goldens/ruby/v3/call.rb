$event_index = 0
def observe_event(actual)
  expected = [1, 1]
  raise "receiver event changed" unless $event_index < 2 && actual == expected[$event_index]
  $event_index += 1
end
def capture(__proto__:)
  observe_event(1); observe_event(__proto__)
  __proto__ + 100
end
def verify_events
  raise "missing receiver events" unless $event_index == 2
end
capture(__proto__: 1)
verify_events()
