module Check
extend self
my_data = {
    "key" => "value \" # not a comment",  # real
}
end
