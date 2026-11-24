import std.json;
void main() {
int capture(T...)(T args) { return 0; }
capture(double.nan, double.infinity, -double.infinity, 1.25, "2024-01-15", 1705322096, "[ordinary text]");
}
