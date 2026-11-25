module Check = struct

type val_t =
  | OFloat of float
  | OArray of val_t array
let my_data : val_t array = [|
    OFloat 5.0e-324;
    OFloat 2.2250738585072014e-308;
    OFloat 1.0e-307;
    OFloat 1.0e+21;
    OFloat (-1.5e+300);
    OFloat 1.7976931348623157e+308;
    OFloat (-1.7976931348623157e+308)
|]

end
