module Fixture_custom_root_multiline_text_Crystal_string_format_multiline_accessor_collision
extend self
fixtureRoot = %q|head
final my_data = 123;
final fakeRoot = 1;
final fixtureRoot = 1;
tail|
end
