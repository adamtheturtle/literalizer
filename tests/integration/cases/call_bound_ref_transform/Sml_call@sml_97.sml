datatype val_t =
    SInt of LargeInt.int
  | SList of val_t list
fun f _ = ()
val ref_data : val_t = SInt 1
val _ = f(ref_data)
