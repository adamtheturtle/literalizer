dynamic check({dynamic timestamp, dynamic date_value}) => null;
final my_data = null;
void main() {
    check(timestamp: DateTime.parse("2024-01-15T10:30:00+00:00"), date_value: DateTime.utc(2024, 6, 1));
}
