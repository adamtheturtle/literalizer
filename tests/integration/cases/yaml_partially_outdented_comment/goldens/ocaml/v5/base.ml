module Check = struct

type val_t =
  | OInt of int
  | OStr of string
  | OList of val_t list
  | OMap of (string * val_t) list
let my_data : val_t = OMap [
    ("a", OMap [
        ("b", OList [OInt 1]);
        (* Outdented from the sequence, so the inner mapping claims this. *)
        ("c", OInt 2)
    ]);
    (* Outdented from the inner mapping too, so the root claims this. *)
    ("d", OInt 3)
]

end
