module Fixture_call_binding_quoted_comment_marker_haxe_Crystal_call
extend self
def make_widget(text = nil); 0; end
my_data = make_widget(text: "first \"quote\"\n// string body") // note
// extra
end
