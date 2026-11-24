module Check = struct

type val_t =
  | OInt of int
let my_data : val_t = OInt (* scalar heading *)
(* second heading line *)
0x2a  (* scalar inline *)
(* inline continuation *)
(* scalar trailing *)

end
