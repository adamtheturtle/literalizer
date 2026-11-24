module Check = struct

type val_t =
  | OFloat of float
  | OList of val_t list
let my_data : val_t = OList [
    OFloat 1.0e-9;
    OFloat (-1.0e-9)
]

end
