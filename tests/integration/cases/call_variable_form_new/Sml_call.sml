fun make_widget _ = ()
datatype val_t =
    SInt of LargeInt.int
val result : val_t = SInt make_widget(42)
val _ = result
