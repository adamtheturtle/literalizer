module Check = struct

type val_t =
  | ODate of (int * int * int)
  | OSet of val_t list
let my_data : val_t = OSet [
    ODate (2024, 1, 15);
    ODate (2024, 6, 1)
]

end
