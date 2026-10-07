module Check = struct

type val_t =
  | OInt of int
  | OFloat of float
  | OList of val_t list
let integer_value : val_t = OFloat 1.0
let my_data : val_t = OList [
    integer_value;
    OFloat 1.5
]

end
