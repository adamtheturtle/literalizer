fun make_widget _ = ()
datatype val_t =
    SInt of LargeInt.int
  | SStr of string
  | SList of val_t list
val _ = make_widget(SList [], SList [SInt 1], SList [])
val _ = make_widget(SList [SStr "text"], SList [SInt 2], SList [])
val _ = make_widget(SList [], SList [SStr "text"], SList [])
val _ = make_widget(SList [SStr "text"], SList [SInt 2], SList [SInt 3])
