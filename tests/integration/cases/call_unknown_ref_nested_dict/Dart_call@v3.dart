dynamic process({dynamic data}) => null;
final my_data = null;
void main() {
    final my_list = <String, String>{
        "unused": "value",
    };
    process(data: <List<Map<String, Map<String, String>>>>[<Map<String, Map<String, String>>>[<String, Map<String, String>>{"inner": my_list}]]);
}
