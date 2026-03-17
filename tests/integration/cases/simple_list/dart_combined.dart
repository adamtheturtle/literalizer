void _declaration() {
  final my_data = [
      1,
      "hello",
      true,
      null,
  ];
  my_data.hashCode;
}
void _assignment() {
  dynamic my_data;
  my_data = [
      1,
      "hello",
      true,
      null,
  ];
  my_data.hashCode;
}
void main() {
  _declaration();
  _assignment();
}
