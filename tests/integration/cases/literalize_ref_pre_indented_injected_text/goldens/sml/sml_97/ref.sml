datatype val_t =
    SInt of LargeInt.int
  | SStr of string
  | SList of val_t list
  | SMap of (string * val_t) list
            val shared : val_t = SList [
                SInt 1,
                SInt 2
            ]
            val other : val_t = SInt 3
            val payload : val_t = SStr "\n    shared : Val\nshared = RInt 99"
            val my_data : val_t = SMap [
                ("a", shared),
                ("b", other),
                ("payload", payload)
            ]
val _ = my_data
