datatype val_t =
    SInt of LargeInt.int
fun make_widget _ = ()
fun consume_widget _ = ()
val my_data = make_widget(SInt 0)
val _ = consume_widget(my_data)
val my_data : val_t = SInt make_widget(SInt 1)
val _ = consume_widget(my_data)
