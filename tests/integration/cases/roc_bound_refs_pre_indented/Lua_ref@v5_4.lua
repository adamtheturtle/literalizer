            local shared = {
                1,
                2,
            }
            local other = 3
            local payload = "\n    shared : Val\nshared = RInt 99"
            local my_data = {
                ["a"] = shared,
                ["b"] = other,
                ["payload"] = payload,
            }
