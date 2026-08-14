module Check = struct

type val_t =
  | OInt of int
  | OStr of string
  | OList of val_t list
  | OMap of (string * val_t) list
let my_data : val_t = OMap [
    ("a", OList [
        OInt 1;
        OInt 2;
        OInt 3
    ]);  (* inline a *)
    ("b", OInt 2)  (* inline b *)
]

end
