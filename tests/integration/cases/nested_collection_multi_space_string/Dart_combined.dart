void _declaration() {
  final my_data = [
      {"key": "hello   world", "value": 1},
  ];
  my_data.hashCode;
}
void _assignment() {
  dynamic my_data;
  my_data = [
      {"key": "hello   world", "value": 1},
  ];
  my_data.hashCode;
}
void main() {
  _declaration();
  _assignment();
}
