module Fixture_call_csharp_conditional_interpolation_binding_Crystal_call
extend self
def make_widget(count = nil); 0; end
my_data = $"{(true ? "// payload" : "ok")}" // trailing
// extra
end
