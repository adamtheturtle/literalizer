datatype val_t =
    SInt of LargeInt.int
fun make_widget _ = ()
val my_data = make_widget(SInt 0)
val my_data : val_t = SInt make_widget(SInt 1)
val _ = make_widget(my_data)
