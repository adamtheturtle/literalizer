module Check = struct

type val_t =
  | OInt of int
  | OStr of string
  | OList of val_t list
  | OMap of (string * val_t) list
let my_data : val_t = OMap [
    (* *)
    (* document heading *)
    (* before the first entry *)
    (* after the key *)
    (* before the value *)
    ("counts", OList [
        (* before the first item *)
        OInt 1;  (* inline block after the comma *)
        (* before the second item *)
        OInt 2
        (* trailing inside the array *)
    ]);  (* after the nested collection *)
    ("more", OList [
        OInt 3;
        (* *)
        (* block heading *)
        (* block continuation *)
        OInt 4  (* final inline *)
    ])
    (* trailing inside the object *)
    (* after the root *)
    (* after the document *)
]

end
