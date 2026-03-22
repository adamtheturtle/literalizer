void _declaration() {
  final my_data = <String, double>{
      "a": 1,
      "b": 2.5,
      "c": 3,
  };
  my_data.hashCode;
}
void _assignment() {
  dynamic my_data;
  my_data = <String, double>{
      "a": 1,
      "b": 2.5,
      "c": 3,
  };
  my_data.hashCode;
}
void main() {
  _declaration();
  _assignment();
}
