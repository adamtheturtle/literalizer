struct Record0 { long quantity; ulong big; double ratio; string label; bool ok; }
void main() {
auto my_data = Record0(
    0b11110100001001000000,
    0b1111111111111111111111111111111111111111111111111111111111111111UL,
    2.5,
    "tag",
    true,
);
}
