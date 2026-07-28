dynamic process({dynamic value}) => null;
final my_data = null;
void main() {
    process(value: "09:30:00");
    process(value: DateTime.parse("2024-01-15T00:00:00+00:00"));
    process(value: 1);
}
