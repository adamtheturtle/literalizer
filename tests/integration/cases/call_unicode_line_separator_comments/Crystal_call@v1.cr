module Fixture_call_unicode_line_separator_comments_Crystal_call
extend self
def process(value = nil); 0; end
process(value: 1);  # note<U+2028>still commented<U+2029>done
end
