void main() {
  {
    final my_data = {
        "name": "Alice",
        "score": null,
        "age": 30,
    };
    my_data.hashCode;
  }
  {
    dynamic my_data;
    my_data = {
        "name": "Alice",
        "score": null,
        "age": 30,
    };
    my_data.hashCode;
  }
}
