fun make_widget _ = ()
datatype val_t =
    SInt of LargeInt.int
val my_data = ($"{(true ? "// payload" : "ok")}").Length >= 0 ? make_widget(SInt 42) : make_widget(SInt 42)
val _ = my_data
