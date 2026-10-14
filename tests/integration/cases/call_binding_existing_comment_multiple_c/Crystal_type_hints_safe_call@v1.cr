module Fixture_call_binding_existing_comment_multiple_c_Crystal_type_hints_safe_call
extend self
def make_widget(count = nil); 0; end
my_data = make_widget(count: 42)
my_data = make_widget(count: my_data) // note
// extra
make_widget(count: my_data);
end
