dynamic process({dynamic data}) => null;
final my_data = null;
void main() {
    final known_value = 1;
    final unknown_value = [];
    process(data: unknown_value);
}
