module Check = struct

type val_t =
  | OInt of int
  | OFloat of float
  | OList of val_t list
let floating_value : val_t = OFloat 1.5
let integer_value : val_t = OFloat 2.0
let my_data : val_t = OList [
    floating_value;
    integer_value
]

end
