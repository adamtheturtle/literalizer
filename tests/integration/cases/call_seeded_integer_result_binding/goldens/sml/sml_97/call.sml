datatype val_t =
    SInt of LargeInt.int
fun make_widget _ = ()
fun consume _ = ()
val my_data = make_widget(SInt 42)
val _ = consume(my_data)
val my_data = make_widget(SInt 42)
val _ = consume(my_data)
