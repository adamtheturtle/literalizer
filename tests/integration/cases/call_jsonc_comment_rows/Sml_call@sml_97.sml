datatype val_t =
    SInt of LargeInt.int
  | SList of val_t list
fun f _ = ()
(* calls heading *)
(* before call one *)
(* first argument *)
val _ = f(SInt 1, SInt 2)  (* after call one *)
(* second argument *)
val _ = f(SInt 3, SInt 4)
(* after all calls *)
