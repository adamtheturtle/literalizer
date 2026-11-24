datatype val_t =
    SInt of LargeInt.int
  | SList of val_t list
fun make_widget _ = ()
fun consume _ = ()
val my_data = make_widget(SInt 42)
val _ = consume(my_data)
