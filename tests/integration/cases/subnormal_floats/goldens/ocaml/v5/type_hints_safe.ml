module Check = struct

type val_t =
  | OFloat of float
  | OList of val_t list
let my_data : val_t = OList [
    OFloat 5.0e-324;
    OFloat (-5.0e-324);
    OFloat 1.0e-310
]

end
