module Check = struct

type val_t =
  | JDate of (int * int * int)
let my_data : val_t = JDate (2024, 1, 15)

end
