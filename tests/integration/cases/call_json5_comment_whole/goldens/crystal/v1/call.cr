module Fixture_call_json5_comment_whole_Crystal_call
extend self
class ReceiverEvents
  @@index = 0
  def self.observe(actual : Int)
    expected = [1, 42]
    raise "receiver event changed" unless @@index < 2 && actual == expected[@@index]
    @@index += 1
  end
  def self.verify
    raise "missing receiver events" unless @@index == 2
  end
end
def f(a : Int)
  ReceiverEvents.observe(1); ReceiverEvents.observe(a)
  a + 100
end
def verify_events
  ReceiverEvents.verify
end
# scalar heading
# second heading line
# scalar inline
# inline continuation
# scalar trailing
f(a: 42);
verify_events();
end
