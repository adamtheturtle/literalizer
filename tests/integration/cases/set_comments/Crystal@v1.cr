require "set"
module Fixture_set_comments_Crystal
extend self
my_data = Set{
    "apple",  # inline comment
    # before banana
    "banana",
    # trailing
}
end
