module Check = struct

type val_t =
  | OFloat of float
  | OList of val_t list
let my_data : val_t = OList [
    OFloat infinity;
    OFloat neg_infinity;
    OFloat nan
]

end
