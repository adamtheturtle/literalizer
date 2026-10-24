module Check = struct

type val_t =
  | OFloat of float
  | OArray of val_t array
let my_data : val_t array = [|
    OFloat (-0.0);
    OFloat 1.5
|]

end
