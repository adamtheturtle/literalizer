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

let my_data : val_t = OMap [
    ("key\nwith\nnewlines", OStr "value1");
    ("key\twith\ttabs", OStr "value2")
]

end
