module Check = struct

type val_t =
  | OInt of int
  | OStr of string
  | OList of val_t list
  | OMap of (string * val_t) list
let my_data : val_t = OMap [
    ("flow", OList [
        OInt 1;
        (* After the first element. *)
        OInt 2
    ]);
    (* Between the key and its value. *)
    ("gap", OInt 3);
    (* On the block scalar header. *)
    ("block", OStr "Text.\n");
    ("anchored", OInt 4);
    ("alias", OInt 4)
    (* On the alias. *)
]

end
