datatype val_t =
    SInt of LargeInt.int
fun make_widget _ = ()
val value : val_t = SInt 1
val _ = make_widget(value)
