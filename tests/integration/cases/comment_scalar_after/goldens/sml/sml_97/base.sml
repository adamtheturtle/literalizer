datatype val_t =
    SInt of LargeInt.int
val my_data : val_t = SInt 42
(* after *)
val _ = my_data
