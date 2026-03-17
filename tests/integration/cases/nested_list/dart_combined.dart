void _declaration() {
  final my_data = [
      true,
      "hi",
      [1, 2],
      null,
  ];
  my_data.hashCode;
}
void _assignment() {
  dynamic my_data;
  my_data = [
      true,
      "hi",
      [1, 2],
      null,
  ];
  my_data.hashCode;
}
void main() {
  _declaration();
  _assignment();
}
