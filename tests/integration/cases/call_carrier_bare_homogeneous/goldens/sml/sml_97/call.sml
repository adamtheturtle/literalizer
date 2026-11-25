fun make_widget _ = ()
datatype val_t =
    SInt of LargeInt.int
  | SList of val_t list
val _ = make_widget(SList [SInt 1], SList [SInt 2])
