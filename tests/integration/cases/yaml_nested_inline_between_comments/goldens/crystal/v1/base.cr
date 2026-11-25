module Fixture_yaml_nested_inline_between_comments_Crystal
extend self
my_data = [
    [2, "hello"],  # trailing note
    # next element
    [3, "world"],
]
end
