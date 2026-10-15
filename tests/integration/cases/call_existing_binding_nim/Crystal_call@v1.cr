module Fixture_call_existing_binding_nim_Crystal_call
extend self
def make_widget(count = nil); 0; end
my_data = make_widget(count: 0)
my_data = make_widget(count: 1)
make_widget(count: my_data);
end
