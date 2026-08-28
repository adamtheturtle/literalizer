datatype val_t =
    SInt of LargeInt.int
  | SList of val_t list
fun process _ = ()
val _ = process(SInt 1)  (* trail \ *)
val _ = process(SInt 2)  (* second *)
