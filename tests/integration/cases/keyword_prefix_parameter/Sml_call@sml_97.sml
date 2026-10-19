fun make_widget _ = ()
datatype val_t =
    SInt of LargeInt.int
val _ = make_widget(SInt 1)
