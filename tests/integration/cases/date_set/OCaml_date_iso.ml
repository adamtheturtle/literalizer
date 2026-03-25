module Check = struct

type val_t =
  | OStr of string
  | OSet of val_t list
let my_data : val_t = OSet [
    OStr "2024-01-15";
    OStr "2024-06-01"
]

end
