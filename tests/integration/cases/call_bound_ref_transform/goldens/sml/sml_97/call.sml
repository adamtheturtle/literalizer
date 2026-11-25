datatype val_t =
    SInt of LargeInt.int
  | SList of val_t list
fun f _ = ()
fun repr _ = ()
val ref_data : val_t = SInt 1
val _ = repr(f(ref_data))
