struct Record0 { bool[] flags; double[] values; long[] ints; string[] text; bool[][] nested_flags; double[][] nested_values; }
void main() {
auto my_data = Record0(
    [
        true,
        false,
    ],
    [
        1.5,
        -2.25,
    ],
    [
        1,
        2,
    ],
    [
        "a",
    ],
    [
        [
            true,
        ],
        [
            false,
        ],
    ],
    [
        [
            1.5,
        ],
        [
            2.25,
        ],
    ],
);
}
