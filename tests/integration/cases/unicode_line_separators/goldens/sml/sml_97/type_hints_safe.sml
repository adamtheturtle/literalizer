datatype val_t =
    SStr of string
val my_data : val_t = SStr "a\194\133b\226\128\168c\226\128\169d\r\226\128\168e"
val _ = my_data
