module Fixture_call_shared_comments_dart_interpolation_comments_new_Crystal_call
extend self
def make_widget(count = nil); 0; end
my_data = ("${ /* } " block */ 42 // } " line
}").length >= 0 ? make_widget(count: 42) : make_widget(count: 42) // trailing
// extra
end
