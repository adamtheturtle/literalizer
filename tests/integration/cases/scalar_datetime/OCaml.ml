type val_t =
  | ONull
  | OBool of bool
  | OInt of int
  | OFloat of float
  | OStr of string
  | OList of val_t list
  | OMap of (string * val_t) list
  | OSet of val_t list
module Check = struct

let x : val_t = OStr "2024-01-15T12:30:00+00:00"

end
