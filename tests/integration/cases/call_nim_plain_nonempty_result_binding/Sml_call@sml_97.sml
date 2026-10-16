fun make_widget _ = ()
datatype val_t =
    SInt of LargeInt.int
  | SList of val_t list
val my_data = make_widget(SList [SInt 1])
val _ = my_data
