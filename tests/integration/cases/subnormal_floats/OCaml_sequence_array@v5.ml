module Check = struct

type val_t =
  | OFloat of float
  | OArray of val_t array
let my_data : val_t array = [|
    OFloat 5.0e-324;
    OFloat (-5.0e-324);
    OFloat 1.0e-310
|]

end
