function consume_widget(...) end
local item = {
    1,
    2,
}
local my_data = {
    1,
    2,
}
consume_widget(my_data)
my_data = item
consume_widget(my_data)
