module Check = struct

type val_t =
  | JFloat of float
  | JList of val_t list
let my_data : val_t = JList [
    JFloat infinity;
    JFloat neg_infinity;
    JFloat nan
]

end
