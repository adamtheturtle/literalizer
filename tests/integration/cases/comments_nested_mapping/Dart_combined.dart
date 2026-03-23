void _declaration() {
  final my_data = {
      "a": <String, int>{"x": 1},
      "b": 2,
  };
  my_data.hashCode;
}
void _assignment() {
  dynamic my_data;
  my_data = {
      "a": <String, int>{"x": 1},
      "b": 2,
  };
  my_data.hashCode;
}
void main() {
  _declaration();
  _assignment();
}
