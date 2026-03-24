void main() {
  {
    final my_data = [
        {"name": "Alice", "age": 30},
        {"name": "Bob", "age": 25},
    ];
    my_data.hashCode;
  }
  {
    dynamic my_data;
    my_data = [
        {"name": "Alice", "age": 30},
        {"name": "Bob", "age": 25},
    ];
    my_data.hashCode;
  }
}
