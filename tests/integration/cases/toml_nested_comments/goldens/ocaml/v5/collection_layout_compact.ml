module Check = struct

type val_t =
  | OInt of int
  | OStr of string
  | OList of val_t list
  | OMap of (string * val_t) list
let my_data : val_t = OMap [
    (* About the first dotted key. *)
    (* About the second dotted key. *)
    ("dotted", OMap [("first", OInt 1); ("second", OInt 2)]);
    ("plain", OInt 3);  (* About the plain key. *)
    (* Before the first entry. *)
    (* Before the second entry. *)
    ("entries", OList [OMap [("name", OStr "one")]; OMap [("name", OStr "two")]]);
    (* Inside the table. *)
    ("table", OMap [("inner", OInt 4)])
]

end
