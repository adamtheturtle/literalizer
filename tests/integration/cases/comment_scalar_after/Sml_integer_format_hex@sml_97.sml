datatype val_t =
    SInt of LargeInt.int
val my_data : val_t = SInt 0x2a
(* after *)
val _ = my_data
