module Check = struct

type val_t =
  | OFloat of float
  | OList of val_t list
let my_data : val_t = OList [
    OFloat 5.0e-324;
    OFloat 2.2250738585072014e-308;
    OFloat 1.0e-307;
    OFloat 1.0e21;
    OFloat (-1.5e300);
    OFloat 1.7976931348623157e308;
    OFloat (-1.7976931348623157e308)
]

end
