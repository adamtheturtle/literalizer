fun make_widget _ = ()
datatype val_t =
    SInt of LargeInt.int
  | SList of val_t list
val my_data = make_widget(SList [SList [SInt 1, SInt 2], SList [SInt 3]])
val _ = my_data
