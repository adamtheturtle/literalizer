module Check = struct

type val_t =
  | ODate of (int * int * int)
let my_data : val_t = ODate (2024, 1, 15)

end
