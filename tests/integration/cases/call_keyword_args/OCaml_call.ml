module Check = struct

type val_t =
  | OFloat of float
  | OStr of string
  | OList of val_t list
print(throttler.check("user_1"; 1000.0))
print(throttler.check("user_2"; 2000.5))

end
