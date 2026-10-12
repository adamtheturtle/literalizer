fun make_widget _ = ()
datatype val_t =
    SStr of string
val my_data = make_widget(SStr "first \"quote\"\n// string body") // note
// extra
val _ = my_data
