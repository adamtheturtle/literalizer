module Check = struct

type val_t =
  | OStr of string
  | OList of val_t list
let process _ = ()
let _ = process(OStr "Dune")  (* first edition *)
let _ = process(OStr "Solaris")
let _ = process(OStr "Neuromancer")  (* cyberpunk *)

end
