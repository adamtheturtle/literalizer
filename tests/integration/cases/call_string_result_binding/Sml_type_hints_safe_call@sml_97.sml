fun make_widget _ = ()
datatype val_t =
    SStr of string
val my_data = make_widget(SStr "text")
val _ = my_data
