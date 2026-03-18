void _declaration() {
  final my_data = {
      "key\nwith\nnewlines": "value1",
      "key\twith\ttabs": "value2",
      "": "value3",
  };
  my_data.hashCode;
}
void _assignment() {
  dynamic my_data;
  my_data = {
      "key\nwith\nnewlines": "value1",
      "key\twith\ttabs": "value2",
      "": "value3",
  };
  my_data.hashCode;
}
void main() {
  _declaration();
  _assignment();
}
