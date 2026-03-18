void _declaration() {
  final my_data = [
      [<int>[1, 2], <String>["a", "b"]],
  ];
  my_data.hashCode;
}
void _assignment() {
  dynamic my_data;
  my_data = [
      [<int>[1, 2], <String>["a", "b"]],
  ];
  my_data.hashCode;
}
void main() {
  _declaration();
  _assignment();
}
