datatype val_t =
    SDatetime of ((int * int * int) * (int * int * int))
val my_data : val_t = SDatetime ((2024, 1, 15), (12, 30, 45))
val _ = my_data
