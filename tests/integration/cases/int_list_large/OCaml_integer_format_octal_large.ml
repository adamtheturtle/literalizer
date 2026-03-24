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
  | ODate of (int * int * int)
  | ODatetime of ((int * int * int) * (int * int * int))

let my_data : val_t = OList [
    OInt 0o3641100;
    OInt (-0o2322);
    OInt 0o377;
    OInt (-0o12)
]

end
