module Fixture_call_comments_Crystal_call
extend self
def process(value = nil); 0; end
# Test cases
process(value: "hello");  # single word
process(value: "hello world");  # two words
# trailing comment
end
