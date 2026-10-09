module [my_data]

Val : [
    RInt I128,
    RStr Str,
    RList (List Val),
    RDict (List (Str, Val)),
]

            shared : Val
            shared = RList [
                RInt 1i128,
                RInt 2i128,
            ]
            other : Val
            other = RInt 3i128
            payload : Val
            payload = RStr "\n    shared : Val\nshared = RInt 99"
            my_data : Val
            my_data = RDict [
                ("a", shared),
                ("b", other),
                ("payload", payload),
            ]
