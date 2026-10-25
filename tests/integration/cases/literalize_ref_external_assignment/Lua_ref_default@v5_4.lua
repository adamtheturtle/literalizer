function consume_widget(...) end
local ref_data = {
    1,
    2,
}
local my_data = {
    0,
}
consume_widget(my_data)
my_data = ref_data
consume_widget(my_data)
