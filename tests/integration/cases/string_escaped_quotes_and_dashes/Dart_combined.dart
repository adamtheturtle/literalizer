void main() {
  {
    final my_data = "hello \"world\" -- not a comment";
    my_data.hashCode;
  }
  {
    dynamic my_data;
    my_data = "hello \"world\" -- not a comment";
    my_data.hashCode;
  }
}
