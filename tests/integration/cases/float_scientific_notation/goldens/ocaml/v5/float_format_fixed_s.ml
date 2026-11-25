module Check = struct

type val_t =
  | OFloat of float
  | OList of val_t list
let my_data : val_t = OList [
    OFloat 0.000000;
    OFloat 1.000000;
    OFloat 1500.000000;
    OFloat 0.001000;
    OFloat 10000000000000000.000000
]

end
