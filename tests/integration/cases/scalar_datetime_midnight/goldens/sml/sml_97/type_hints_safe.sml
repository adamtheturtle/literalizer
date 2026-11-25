datatype val_t =
    SDatetime of ((int * int * int) * (int * int * int))
val my_data : val_t = SDatetime ((2024, 1, 15), (0, 0, 0))
val _ = my_data
