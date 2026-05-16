module Check = struct

type val_t =
  | OStr of string
  | OList of val_t list
let process _ = ()
let _ = process("Dune")  (* first edition *)
let _ = process("Solaris")
let _ = process("Neuromancer")  (* cyberpunk *)

end
