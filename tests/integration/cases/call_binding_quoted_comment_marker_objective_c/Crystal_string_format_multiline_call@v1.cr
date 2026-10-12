module Fixture_call_binding_quoted_comment_marker_objective_c_Crystal_string_format_multiline_call
extend self
def make_widget(text = nil); 0; end
my_data = make_widget(text: %q|first "quote"
// string body|) // note
// extra
end
