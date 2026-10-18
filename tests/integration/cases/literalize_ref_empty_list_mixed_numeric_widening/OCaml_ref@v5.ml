module Check = struct

type val_t =
  | OInt of int
  | OFloat of float
  | OList of val_t list
let empty_values : val_t = OList []
let integer_values : val_t = OList [
    OInt 1
]
let float_values : val_t = OList [
    OFloat 1.5
]
let my_data : val_t = OList [
    empty_values;
    integer_values;
    float_values
]

end
