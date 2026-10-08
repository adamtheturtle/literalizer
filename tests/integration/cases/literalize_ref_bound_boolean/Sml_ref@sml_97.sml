datatype val_t =
    SBool of bool
val ref_flag : val_t = SBool true
val my_data : val_t = ref_flag
val _ = my_data
