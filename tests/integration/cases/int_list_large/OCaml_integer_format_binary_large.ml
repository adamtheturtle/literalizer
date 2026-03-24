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
    OInt 0b11110100001001000000;
    OInt (-0b10011010010);
    OInt 0b11111111;
    OInt (-0b1010)
]

end
