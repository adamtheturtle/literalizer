function consume_widget(...) end
local shared = {
    1,
    2,
}
local my_data = shared
consume_widget(my_data)
