module Check = struct

type val_t =
  | OFloat of float
  | OList of val_t list
let my_data : val_t = OList [
    OFloat 1.100000;
    OFloat (-2.200000);
    OFloat 3.300000
]

end
