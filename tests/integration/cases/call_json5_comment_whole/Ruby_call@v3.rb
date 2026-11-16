$event_index = 0
def observe_event(actual)
  expected = [1, 42]
  raise "receiver event changed" unless $event_index < 2 && actual == expected[$event_index]
  $event_index += 1
end
def f(a:)
  observe_event(1); observe_event(a)
  a + 100
end
def verify_events
  raise "missing receiver events" unless $event_index == 2
end
# scalar heading
# second heading line
# scalar inline
# inline continuation
# scalar trailing
f(a: 42)
verify_events()
