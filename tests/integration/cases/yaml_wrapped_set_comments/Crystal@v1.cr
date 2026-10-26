require "set"
module Fixture_yaml_wrapped_set_comments_Crystal
extend self
my_data = Set{
    10,  # comment for ten
    2,  # comment for two
}
end
