datatype val_t =
    SInt of LargeInt.int
val my_data : val_t = SInt 0x80000000
val _ = my_data
