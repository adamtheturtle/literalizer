module Check = struct

type val_t =
  | OInt of int
  | OStr of string
  | OList of val_t list
  | OMap of (string * val_t) list
let my_data : val_t = OMap [
    ("a", OMap [
        (* inner note *)
        ("b", OInt 1)  (* inline b *)
    ]);
    ("list", OList [
        OInt 1;  (* first *)
        OInt 2  (* second *)
    ])
]

end
