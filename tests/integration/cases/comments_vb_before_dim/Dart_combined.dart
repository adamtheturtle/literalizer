void _declaration() {
  final my_data = {
      // Configuration
      "name": "app",
      // Port setting
      "port": 3000,
  };
  my_data.hashCode;
}
void _assignment() {
  dynamic my_data;
  my_data = {
      // Configuration
      "name": "app",
      // Port setting
      "port": 3000,
  };
  my_data.hashCode;
}
void main() {
  _declaration();
  _assignment();
}
