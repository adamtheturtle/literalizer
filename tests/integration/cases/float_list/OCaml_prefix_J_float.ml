module Check = struct

type val_t =
  | JFloat of float
  | JList of val_t list
let my_data : val_t = JList [
    JFloat 1.1;
    JFloat (-2.2);
    JFloat 3.3
]

end
