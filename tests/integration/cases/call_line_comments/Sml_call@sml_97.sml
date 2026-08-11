datatype val_t =
    SStr of string
  | SList of val_t list
fun process _ = ()
val _ = process(SStr "Dune")  (* first edition *)
val _ = process(SStr "Solaris")
val _ = process(SStr "Neuromancer")  (* cyberpunk *)
