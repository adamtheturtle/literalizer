require "set"
module Fixture_set_comments_crystal
extend self
my_data = Set{
    "apple",  # inline comment
    # before banana
    "banana",
    # trailing
}
end
