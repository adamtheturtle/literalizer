module Check = struct

module App = struct
module Process = struct
let fetch _ = ()
end
end
type val_t =
  | OBool of bool
  | OInt of int
  | OStr of string
  | OList of val_t list
  | OMap of (string * val_t) list
let _ = App.Process.fetch(OMap [("data", OStr "hello")])
let _ = App.Process.fetch(OMap [("data", OInt 42)])
let _ = App.Process.fetch(OMap [("data", OBool true)])

end
