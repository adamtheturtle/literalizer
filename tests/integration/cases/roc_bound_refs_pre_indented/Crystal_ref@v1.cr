module Fixture_roc_bound_refs_pre_indented_Crystal_ref
extend self
            shared = [
                1,
                2,
            ]
            other = 3
            payload = "\n    shared : Val\nshared = RInt 99"
            my_data = {
                "a" => shared,
                "b" => other,
                "payload" => payload,
            }
end
