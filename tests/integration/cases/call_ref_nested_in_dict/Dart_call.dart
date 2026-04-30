dynamic process({dynamic data}) => null;
final my_data = null;
void main() {
    final my_var = 42;
    process(data: <String, int>{"key": my_var, "count": 42});
}
