module Fixture_literalize_ref_deep_nesting_Crystal_ref
extend self
deep = [
    [
        1,
        2,
    ],
    [
        3,
        4,
    ],
]
my_data = {
    "a" => {
        "b" => {
            "c" => deep,
        },
    },
}
end
