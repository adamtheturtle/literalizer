module Check = struct

type val_t =
  | OInt of int
let my_data : val_t = OInt (* scalar heading *)
(* second heading line *)
0b101010  (* scalar inline *)
(* inline continuation *)
(* scalar trailing *)

end
