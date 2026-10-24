datatype val_t =
    SDatetime of ((int * int * int) * (int * int * int))
val my_data : val_t = SDatetime ((2099, 6, 15), (8, 30, 0))
val _ = my_data
