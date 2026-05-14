module Check = struct

type val_t =
  | OStr of string
let my_data : val_t = OStr (* before *)
"plain"  (* inline *)

end
