fun make_widget _ = ()
datatype val_t =
    SInt of LargeInt.int
val my_data = (`__LINE__ > 0) ? make_widget(SInt 42) : make_widget(SInt 42) // trailing `marker
val _ = my_data
