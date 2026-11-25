datatype val_t =
    SList of val_t list
fun make_widget _ = ()
val items : val_t = SList []
val _ = make_widget(items)
