module Fixture_call_binding_quoted_comment_marker_c_Crystal_type_hints_safe_call
extend self
def make_widget(text = nil); 0; end
my_data = make_widget(text: "first \"quote\"\n// string body") // note
// extra
end
