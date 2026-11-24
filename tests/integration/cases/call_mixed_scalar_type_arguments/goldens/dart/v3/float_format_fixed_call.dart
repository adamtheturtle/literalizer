dynamic capture({dynamic nan_value, dynamic positive_infinity, dynamic negative_infinity, dynamic finite_value, dynamic date_value, dynamic datetime_value, dynamic text_value}) => null;
final my_data = null;
void main() {
    capture(nan_value: double.nan, positive_infinity: double.infinity, negative_infinity: double.negativeInfinity, finite_value: 1.250000, date_value: DateTime.utc(2024, 1, 15), datetime_value: DateTime.utc(2024, 1, 15, 12, 34, 56), text_value: "[ordinary text]");
}
