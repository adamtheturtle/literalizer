datatype val_t =
    SInt of LargeInt.int
  | SList of val_t list
fun f _ = ()
(* selected heading *)
val _ = f(SInt 1, SInt 2)  (* selected inline *)
