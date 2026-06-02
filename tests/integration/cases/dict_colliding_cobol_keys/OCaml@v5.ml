module Check = struct

type val_t =
  | OInt of int
  | OStr of string
  | OMap of (string * val_t) list
let my_data : val_t = OMap [
    ("user_name", OInt 1);
    ("user.name", OInt 2);
    ("user-name", OInt 3);
    ("field_name_that_is_really_quite_long_one", OInt 4);
    ("field_name_that_is_really_quite_long_two", OInt 5)
]

end
