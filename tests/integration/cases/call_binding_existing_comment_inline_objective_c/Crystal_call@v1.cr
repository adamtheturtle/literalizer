module Fixture_call_binding_existing_comment_inline_objective_c_Crystal_call
extend self
def make_widget(count = nil); 0; end
my_data = 42
my_data = make_widget(count: my_data) // note
make_widget(count: my_data);
end
