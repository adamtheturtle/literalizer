module Check = struct

type val_t =
  | JFloat of float
  | JList of val_t list
let my_data : val_t = JList [
    JFloat 1.0e-09;
    JFloat (-1.0e-09)
]

end
