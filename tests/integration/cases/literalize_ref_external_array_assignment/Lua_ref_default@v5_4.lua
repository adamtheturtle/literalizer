function consume_widget(...) end
local shared = {
    1,
    2,
}
local my_data = {
    0,
}
consume_widget(my_data)
my_data = shared
consume_widget(my_data)
