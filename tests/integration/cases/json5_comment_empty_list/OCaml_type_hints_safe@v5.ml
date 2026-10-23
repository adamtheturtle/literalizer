module Check = struct

type val_t =
  | OList of val_t list
(* empty heading *)
(* empty body *)
(* after empty *)
let my_data : val_t = OList []

end
