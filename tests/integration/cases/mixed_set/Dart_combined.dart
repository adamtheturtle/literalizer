void main() {
  {
    final my_data = {
        true,
        42,
        "apple",
    };
    my_data.hashCode;
  }
  {
    dynamic my_data;
    my_data = {
        true,
        42,
        "apple",
    };
    my_data.hashCode;
  }
}
