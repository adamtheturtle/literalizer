void main() {
  {
    final my_data = <String, String>{
        "message": "no comment here",
    };
    my_data.hashCode;
  }
  {
    dynamic my_data;
    my_data = <String, String>{
        "message": "no comment here",
    };
    my_data.hashCode;
  }
}
