datatype val_t =
    SStr of string
  | SList of val_t list
fun process _ = ()
val _ = process("Dune")  (* first edition *)
val _ = process("Solaris")
val _ = process("Neuromancer")  (* cyberpunk *)
