module Main

            type Val =
                | FInt of int64
                | FStr of string
                | FList of Val list
                | FMap of (string * Val) list
            let shared: Val = FList [
                FInt 1L;
                FInt 2L
            ]
            let other: Val = FInt 3L
            let payload: Val = FStr "\n    shared : Val\nshared = RInt 99"
            let my_data: Val = FMap [
                ("a", shared);
                ("b", other);
                ("payload", payload)
            ]
