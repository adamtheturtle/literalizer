module Fixture_call_binding_inner_comment_zig_Crystal_call
extend self
def make_widget(count = nil); 0; end
my_data = (
make_widget(count: 42) // inner
) // trailing
end
