datatype val_t =
    SNull
  | SInt of LargeInt.int
fun make_widget _ = ()
val my_data : val_t = SNull
val my_data : val_t = SInt make_widget(SInt 42) // note
