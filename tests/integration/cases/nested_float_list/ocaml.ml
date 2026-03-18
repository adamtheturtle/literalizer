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

let x : val_t = OList [
    OList [OFloat 1.5; OFloat 2.5];
    OList [OFloat 3.5; OFloat 4.5]
]

end
