datatype val_t =
    SInt of LargeInt.int
val my_data : val_t = SInt 42  (* note *)
val _ = my_data
