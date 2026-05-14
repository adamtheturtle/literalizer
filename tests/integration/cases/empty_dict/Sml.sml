datatype val_t =
    SMap of (string * val_t) list
val my_data : val_t = SMap []
val _ = my_data
