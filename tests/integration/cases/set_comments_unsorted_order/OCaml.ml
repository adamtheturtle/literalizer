module Check = struct

type val_t =
  | ONull
  | OBool of bool
  | OInt of int
  | OFloat of float
  | OStr of string
  | OList of val_t list
  | OMap of (string * val_t) list
  | OSet of val_t list

let x : val_t = OSet [
    (* before apple *)
    OStr "apple";
    OStr "banana"  (* banana inline *)
    (* trailing *)
]

end
