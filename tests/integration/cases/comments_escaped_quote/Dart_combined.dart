void main() {
  {
    final my_data = <String, String>{
        "key": "value \" # not a comment",  // real
    };
    my_data.hashCode;
  }
  {
    dynamic my_data;
    my_data = <String, String>{
        "key": "value \" # not a comment",  // real
    };
    my_data.hashCode;
  }
}
