fun make_widget _ = ()
datatype val_t =
    SInt of LargeInt.int
val my_data = (~/\//).match("/") ? make_widget(SInt 42) : null
val _ = my_data
