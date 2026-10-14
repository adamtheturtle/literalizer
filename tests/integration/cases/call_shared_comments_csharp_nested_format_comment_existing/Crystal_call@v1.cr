module Fixture_call_shared_comments_csharp_nested_format_comment_existing_Crystal_call
extend self
def make_widget(count = nil); 0; end
my_data = make_widget(count: nil)
my_data = ($"{$"{1://}"}").Length >= 0 ? make_widget(count: 42) : make_widget(count: 42) // trailing
// extra
end
