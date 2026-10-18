fun make_widget _ = ()
datatype val_t =
    SInt of LargeInt.int
  | SStr of string
  | SList of val_t list
val _ = make_widget(SList [SInt 1], SList [SStr "text"])
