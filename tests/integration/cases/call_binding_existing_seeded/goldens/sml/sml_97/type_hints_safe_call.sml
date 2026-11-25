datatype val_t =
    SInt of LargeInt.int
fun make_widget _ = ()
val my_data = make_widget(SInt 42)
val _ = make_widget(my_data)
val my_data = make_widget(my_data)
val _ = make_widget(my_data)
