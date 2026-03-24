void main() {
  {
    final my_data = {
        "name": "Alice",
        "age": 30,
        "active": true,
        "score": null,
    };
    my_data.hashCode;
  }
  {
    dynamic my_data;
    my_data = {
        "name": "Alice",
        "age": 30,
        "active": true,
        "score": null,
    };
    my_data.hashCode;
  }
}
