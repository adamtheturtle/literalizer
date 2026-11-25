struct Record0 { string title; string[] tags; long priority; }
void main() {
auto my_data = Record0(
    "report",
    [
        "draft",
        "urgent",
        "review",
    ],
    2,
);
}
