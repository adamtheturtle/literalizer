struct Record0 { long id; string description; bool is_done; long[] blocks; }
void main() {
auto my_data = Record0(
    1,
    "She said \"hello\", then waved",
    false,
    [
        1,
        2,
        3,
    ],
);
}
