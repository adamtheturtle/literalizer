fun make_widget _ = ()
datatype val_t =
    SInt of LargeInt.int
val my_data = make_widget(SInt 1)
val _ = my_data
