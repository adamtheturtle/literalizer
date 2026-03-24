void main() {
  {
    final my_data = {
        // Server configuration
        "host": "localhost",  // default host
        "port": 8080,
        // Enable debug mode
        "debug": true,
    };
    my_data.hashCode;
  }
  {
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
}
