module Fixture_call_sv_macro_binding_comment_Crystal_call
extend self
def make_widget(count = nil); 0; end
my_data = (`__LINE__ > 0) ? make_widget(count: 42) : make_widget(count: 42) // trailing `marker
end
