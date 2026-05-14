module Fixture_call_ref_args_escaped_quote_Crystal_call
extend self
def process(v = nil); 0; end
my_str = "a\"b"
process(v: my_str);
end
