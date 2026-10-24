module Check = struct

type val_t =
  | OStr of string
  | OMap of (string * val_t) list
(* empty heading *)
(* empty body *)
(* after empty *)
let my_data : val_t = OMap []

end
