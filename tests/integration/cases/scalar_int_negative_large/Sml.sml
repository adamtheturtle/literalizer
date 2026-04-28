datatype val_t =
    SInt of LargeInt.int
val my_data : val_t = SInt (~2147483649)
val _ = my_data
