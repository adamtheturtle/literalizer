datatype val_t =
    SInt of LargeInt.int
fun f _ = ()
(* scalar heading *)
(* second heading line *)
(* scalar inline *)
(* inline continuation *)
(* scalar trailing *)
val _ = f(SInt 42)
