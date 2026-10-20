module Fixture_call_dotted_empty_result_binding_Crystal_heterogeneous_strategy_record_call
extend self
class ThingType_; def go(value = nil); 0; end; end
thing = ThingType_.new
my_data = thing.go(value: [] of Nil)
end
