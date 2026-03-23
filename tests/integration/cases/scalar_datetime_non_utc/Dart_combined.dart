void _declaration() {
  final my_data = DateTime.parse("2024-01-15T18:00:00+05:30");
  my_data.hashCode;
}
void _assignment() {
  dynamic my_data;
  my_data = DateTime.parse("2024-01-15T18:00:00+05:30");
  my_data.hashCode;
}
void main() {
  _declaration();
  _assignment();
}
