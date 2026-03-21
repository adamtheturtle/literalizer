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
    OStr "2024-01-15T12:30:00+00:00";
    OStr "2024-06-30T08:00:00+00:00";
    OStr "2024-12-25T18:45:00+00:00"
]

end
