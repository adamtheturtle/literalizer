dynamic process({dynamic known_value, dynamic nested_missing}) => null;
final my_data = null;
void main() {
    final known_value = true;
    final unknown_value = true;
    process(known_value: known_value, nested_missing: unknown_value);
}
