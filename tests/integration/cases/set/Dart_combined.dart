void main() {
  {
    final my_data = {
        "apple",
        "banana",
        "cherry",
    };
    my_data.hashCode;
  }
  {
    dynamic my_data;
    my_data = {
        "apple",
        "banana",
        "cherry",
    };
    my_data.hashCode;
  }
}
