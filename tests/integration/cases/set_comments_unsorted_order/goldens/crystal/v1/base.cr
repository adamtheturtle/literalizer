require "set"
module Fixture_set_comments_unsorted_order_Crystal
extend self
my_data = Set{
    # before apple
    "apple",
    "banana",  # banana inline
    # trailing
}
end
