module Check = struct

type val_t =
  | OInt of int
  | OFloat of float
  | OList of val_t list
let my_data : val_t = OList [
    OInt (-42);
    OInt 0;
    OInt 42;
    OFloat (-1.250000);
    OFloat 0.000000;
    OFloat 1.250000
]

end
