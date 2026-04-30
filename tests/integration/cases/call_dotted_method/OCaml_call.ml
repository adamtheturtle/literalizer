module Check = struct

type val_t =
  | OBool of bool
  | OInt of int
  | OStr of string
  | OList of val_t list
module App = struct
module Client = struct
let fetch _ = ()
end
end
let _ = App.Client.fetch("hello")
let _ = App.Client.fetch(42)
let _ = App.Client.fetch(OBool true)

end
