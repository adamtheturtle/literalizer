datatype val_t =
    SInt of LargeInt.int
fun make_widget _ = ()
val my_data : val_t = SInt 42
val my_data : val_t = make_widget(my_data) // note
val _ = make_widget(my_data)
