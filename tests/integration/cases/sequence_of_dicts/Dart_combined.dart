void _declaration() {
  final my_data = [
      {"name": "Alice", "age": 30},
      {"name": "Bob", "age": 25},
  ];
  my_data.hashCode;
}
void _assignment() {
  dynamic my_data;
  my_data = [
      {"name": "Alice", "age": 30},
      {"name": "Bob", "age": 25},
  ];
  my_data.hashCode;
}
void main() {
  _declaration();
  _assignment();
}
