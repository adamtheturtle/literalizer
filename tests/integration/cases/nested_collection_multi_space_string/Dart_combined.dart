void main() {
  {
    final my_data = [
        {"key": "hello   world", "value": 1},
    ];
    my_data.hashCode;
  }
  {
    dynamic my_data;
    my_data = [
        {"key": "hello   world", "value": 1},
    ];
    my_data.hashCode;
  }
}
