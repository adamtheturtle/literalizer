fun make_widget _ = ()
datatype val_t =
    SList of val_t list
val _ = make_widget(SList [])
