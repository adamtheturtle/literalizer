datatype val_t =
    SInt of LargeInt.int
val stamp : val_t = SInt 1
val result_data : val_t = stamp
val _ = result_data
