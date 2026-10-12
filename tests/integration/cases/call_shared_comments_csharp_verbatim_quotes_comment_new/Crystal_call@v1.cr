module Fixture_call_shared_comments_csharp_verbatim_quotes_comment_new_Crystal_call
extend self
def make_widget(count = nil); 0; end
my_data = (@"a"" // payload""b").Length >= 0 ? make_widget(count: 42) : make_widget(count: 42) // trailing
// extra
end
