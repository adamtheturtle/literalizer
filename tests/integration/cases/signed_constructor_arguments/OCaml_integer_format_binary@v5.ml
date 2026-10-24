module Check = struct

type val_t =
  | OInt of int
  | OFloat of float
  | OList of val_t list
let my_data : val_t = OList [
    OInt (-0b101010);
    OInt 0b0;
    OInt 0b101010;
    OFloat (-1.25);
    OFloat 0.0;
    OFloat 1.25
]

end
