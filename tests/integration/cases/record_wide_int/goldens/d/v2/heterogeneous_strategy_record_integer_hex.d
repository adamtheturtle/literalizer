struct Record0 { long quantity; ulong big; double ratio; string label; bool ok; }
void main() {
auto my_data = Record0(
    0xf4240,
    0xffffffffffffffffUL,
    2.5,
    "tag",
    true,
);
}
