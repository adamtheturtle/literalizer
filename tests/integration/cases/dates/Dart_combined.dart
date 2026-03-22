void _declaration() {
  final my_data = {
      "date": DateTime.parse("2024-01-15"),
      "datetime": DateTime.parse("2024-01-15T12:30:00+00:00"),
  };
  my_data.hashCode;
}
void _assignment() {
  dynamic my_data;
  my_data = {
      "date": DateTime.parse("2024-01-15"),
      "datetime": DateTime.parse("2024-01-15T12:30:00+00:00"),
  };
  my_data.hashCode;
}
void main() {
  _declaration();
  _assignment();
}
