fun make_widget _ = ()
datatype val_t =
    SInt of LargeInt.int
val my_data = "${{'value': '// payload'}['value']}" // trailing
// extra
val _ = my_data
