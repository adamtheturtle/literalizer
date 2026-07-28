dynamic process({dynamic data}) => null;
final my_data = null;
void main() {
    final my_list = [];
    process(data: <List<Map<String, Map<String, String>>>>[<Map<String, Map<String, String>>>[<String, Map<String, String>>{"inner": my_list}]]);
}
