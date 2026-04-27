require "set"
module Fixture_set_comments_unsorted_order_crystal
extend self
my_data = Set{
    # before apple
    "apple",
    "banana",  # banana inline
    # trailing
}
end
