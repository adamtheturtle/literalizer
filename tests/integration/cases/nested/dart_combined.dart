void _declaration() {
  final my_data = {
      "users": [{"name": "Bob", "tags": ["admin", "user"]}, {"name": "Carol", "tags": ["guest"]}],
  };
  my_data.hashCode;
}
void _assignment() {
  dynamic my_data;
  my_data = {
      "users": [{"name": "Bob", "tags": ["admin", "user"]}, {"name": "Carol", "tags": ["guest"]}],
  };
  my_data.hashCode;
}
void main() {
  _declaration();
  _assignment();
}
