datatype val_t =
    SInt of LargeInt.int
val my_int : val_t = SInt 42
val my_data : val_t = my_int
val _ = my_data
