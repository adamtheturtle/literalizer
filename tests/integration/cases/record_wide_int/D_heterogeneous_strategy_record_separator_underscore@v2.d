struct Record0 { long quantity; ulong big; double ratio; string label; bool ok; }
void main() {
auto my_data = Record0(
    1_000_000,
    18_446_744_073_709_551_615UL,
    2.5,
    "tag",
    true,
);
}
