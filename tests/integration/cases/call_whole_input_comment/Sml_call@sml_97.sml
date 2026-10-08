datatype val_t =
    SInt of LargeInt.int
  | SList of val_t list
fun f _ = ()
val _ = f(SList [SInt 1])  (* note *)
