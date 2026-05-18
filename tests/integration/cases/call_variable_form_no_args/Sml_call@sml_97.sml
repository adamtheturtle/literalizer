fun make_widget _ = ()
datatype val_t =
    SList of val_t list
val my_data = make_widget()
val _ = my_data
