datatype val_t =
    SDatetime of ((int * int * int) * (int * int * int))
val my_data : val_t = SDatetime ((1901, 12, 13), (20, 45, 51))
val _ = my_data
