module Fixture_call_binding_existing_comment_multiple_java_Crystal_type_hints_safe_call
extend self
def make_widget(count = nil); 0; end
my_data = make_widget(count: nil)
my_data = make_widget(count: 42) // note
// extra
end
