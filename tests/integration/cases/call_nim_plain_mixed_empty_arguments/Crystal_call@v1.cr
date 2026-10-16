module Fixture_call_nim_plain_mixed_empty_arguments_Crystal_call
extend self
def make_widget(before = nil, populated = nil, after = nil); 0; end
make_widget(before: [] of Nil, populated: [1], after: [] of Nil);
make_widget(before: ["text"], populated: [2], after: [] of Nil);
make_widget(before: [] of Nil, populated: ["text"], after: [] of Nil);
make_widget(before: ["text"], populated: [2], after: [3]);
end
