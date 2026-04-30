dynamic process({dynamic data}) => null;
final my_data = null;
void main() {
    final my_var = 42;
    final my_other = 7;
    process(data: [my_var, 42, "static"]);
    process(data: [my_other, 7, "label"]);
}
