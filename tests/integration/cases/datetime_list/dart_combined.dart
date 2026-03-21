void _declaration() {
  final my_data = [
      DateTime.parse("2024-01-15T12:30:00+00:00"),
      DateTime.parse("2024-06-30T08:00:00+00:00"),
      DateTime.parse("2024-12-25T18:45:00+00:00"),
  ];
  my_data.hashCode;
}
void _assignment() {
  dynamic my_data;
  my_data = [
      DateTime.parse("2024-01-15T12:30:00+00:00"),
      DateTime.parse("2024-06-30T08:00:00+00:00"),
      DateTime.parse("2024-12-25T18:45:00+00:00"),
  ];
  my_data.hashCode;
}
void main() {
  _declaration();
  _assignment();
}
