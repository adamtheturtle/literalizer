datatype val_t =
    SList of val_t list
fun consume_widget _ = ()
val item : val_t = SList []
val my_data : val_t = SList [
    item,
    item
]
val _ = consume_widget(my_data)
