            set shared [list \
                1 \
                2 \
            ]
            set other 3
            set payload "\n    shared : Val\nshared = RInt 99"
            set my_data [dict create \
                "a" shared \
                "b" other \
                "payload" payload \
            ]
