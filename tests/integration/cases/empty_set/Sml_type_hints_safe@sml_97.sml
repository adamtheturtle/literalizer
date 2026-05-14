datatype val_t =
    SSet of val_t list
val my_data : val_t = SSet []
val _ = my_data
