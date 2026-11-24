module Check = struct

type val_t =
  | OFloat of float
  | OList of val_t list
let my_data : val_t = OList [
    OFloat 1.1;
    OFloat (-2.2);
    OFloat 3.3
]

end
