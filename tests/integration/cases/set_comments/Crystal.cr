require "set"
module Check
extend self
my_data = Set{
    "apple",  # inline comment
    # before banana
    "banana",
    # trailing
}
end
