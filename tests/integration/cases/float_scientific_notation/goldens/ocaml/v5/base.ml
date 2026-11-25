module Check = struct

type val_t =
  | OFloat of float
  | OList of val_t list
let my_data : val_t = OList [
    OFloat 0.0;
    OFloat 1.0;
    OFloat 1500.0;
    OFloat 0.001;
    OFloat 1.0e+16
]

end
