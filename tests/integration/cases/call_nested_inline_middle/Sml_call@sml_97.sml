datatype val_t =
    SStr of string
  | SList of val_t list
fun f _ = ()
val _ = f(SList [SList [SStr "DEL", SStr "b", SStr "10"], SList [SStr "ADD", SStr "a", SStr "x"]])  (* note *)
