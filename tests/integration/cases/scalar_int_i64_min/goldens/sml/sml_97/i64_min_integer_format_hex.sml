datatype val_t =
    SInt of LargeInt.int
val my_data : val_t = SInt (~0x8000000000000000)
val _ = my_data
