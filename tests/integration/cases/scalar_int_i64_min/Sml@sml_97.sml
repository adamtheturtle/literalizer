datatype val_t =
    SInt of LargeInt.int
val my_data : val_t = SInt (~9223372036854775808)
val _ = my_data
