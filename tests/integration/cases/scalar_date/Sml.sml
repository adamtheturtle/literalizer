datatype val_t =
    SDate of (int * int * int)
val my_data : val_t = SDate (2024, 1, 15)
val _ = my_data
