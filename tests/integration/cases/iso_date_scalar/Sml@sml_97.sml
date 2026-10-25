datatype val_t =
    SDate of (int * int * int)
val my_data : val_t = SDate (2000, 1, 1)
val _ = my_data
