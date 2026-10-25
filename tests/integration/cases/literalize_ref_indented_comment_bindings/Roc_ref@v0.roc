module [my_data]

Val : [
    RInt I128,
    RStr Str,
    RList (List Val),
]

        shared : Val
        shared = RList [
            RInt 1i128,
            RInt 2i128,
        ]
        my_data : Val
        my_data = RList [
            # A leading comment with { braces, "quotes", and // markers
            RStr "first\n{ \"quoted\" // text }",
            shared,
        ]
