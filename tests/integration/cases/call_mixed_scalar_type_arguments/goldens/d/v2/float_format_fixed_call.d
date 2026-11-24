import std.json;
void main() {
int capture(T...)(T args) { return 0; }
capture(double.nan, double.infinity, -double.infinity, 1.250000, "2024-01-15", "2024-01-15T12:34:56", "[ordinary text]");
}
