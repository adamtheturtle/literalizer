datatype val_t =
    SStr of string
val my_data : val_t = SStr "\nroot first line\n  indented\n\nroot last line\n"
val _ = my_data
