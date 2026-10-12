module Fixture_call_shared_comments_csharp_conditional_plain_new_Crystal_call
extend self
def make_widget(count = nil); 0; end
my_data = ($"{(true ? "// payload" : "ok")}").Length >= 0 ? make_widget(count: 42) : make_widget(count: 42)
end
