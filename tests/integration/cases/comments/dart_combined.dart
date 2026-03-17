void _declaration() {
  final my_data = {
      // Server configuration
      "host": "localhost",  // default host
      "port": 8080,
      // Enable debug mode
      "debug": true,
  };
  my_data.hashCode;
}
void _assignment() {
  dynamic my_data;
  my_data = {
      // Server configuration
      "host": "localhost",  // default host
      "port": 8080,
      // Enable debug mode
      "debug": true,
  };
  my_data.hashCode;
}
void main() {
  _declaration();
  _assignment();
}
