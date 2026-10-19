module Check = struct

type val_t =
  | OInt of int
  | OFloat of float
  | OStr of string
  | OList of val_t list
let my_data : val_t = OList [
    OInt 1;
    OStr "a";
    OFloat 2.5
]

end
