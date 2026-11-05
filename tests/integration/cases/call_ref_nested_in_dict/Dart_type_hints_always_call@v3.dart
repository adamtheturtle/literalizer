dynamic process({dynamic data}) => null;
final my_data = null;
void main() {
    final int my_var = 42;
    process(data: <String, dynamic>{"key": my_var, "count": 42, "label": "example"});
}
