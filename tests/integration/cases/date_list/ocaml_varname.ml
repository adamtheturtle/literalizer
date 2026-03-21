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

let my_data : val_t = OList [
    OStr "2024-01-15";
    OStr "2024-06-30";
    OStr "2024-12-25"
]

end
