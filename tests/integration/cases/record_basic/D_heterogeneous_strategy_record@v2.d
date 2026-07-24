struct Record0 { long id; string label; bool enabled; long[] related_ids; }
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
