module Fixture_call_bound_ref_multiline_layout_Crystal_call
extend self
def f(value = nil); 0; end
x = [
    [
        1,
        2,
    ],
    [
        3,
        4,
    ],
]
f(value: [
    [
        x,
    ],
]);
end
