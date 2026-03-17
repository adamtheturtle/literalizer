void _declaration() {
  final my_data = {
      "apple",
      "banana",
      "cherry",
  };
  my_data.hashCode;
}
void _assignment() {
  dynamic my_data;
  my_data = {
      "apple",
      "banana",
      "cherry",
  };
  my_data.hashCode;
}
void main() {
  _declaration();
  _assignment();
}
