datatype val_t =
    SStr of string
val my_data : val_t = SStr "hello \"world\" -- not a comment"
val _ = my_data
