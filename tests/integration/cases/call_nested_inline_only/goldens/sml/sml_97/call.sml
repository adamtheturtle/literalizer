datatype val_t =
    SInt of LargeInt.int
  | SStr of string
  | SList of val_t list
fun f _ = ()
val _ = f(SInt 2, SStr "hello")  (* trailing note *)
val _ = f(SInt 3, SStr "world")  (* another note *)
