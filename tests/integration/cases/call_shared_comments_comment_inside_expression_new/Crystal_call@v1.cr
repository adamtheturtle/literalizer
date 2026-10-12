module Fixture_call_shared_comments_comment_inside_expression_new_Crystal_call
extend self
def make_widget(count = nil); 0; end
my_data = make_widget(count: 42) // inner
 + 1
end
