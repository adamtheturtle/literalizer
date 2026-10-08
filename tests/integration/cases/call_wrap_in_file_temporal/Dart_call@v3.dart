dynamic check({dynamic ts, dynamic d}) => null;
final my_data = null;
void main() {
    check(ts: DateTime.parse("2024-01-15T10:30:00+00:00"), d: DateTime.utc(2024, 6, 1));
}
