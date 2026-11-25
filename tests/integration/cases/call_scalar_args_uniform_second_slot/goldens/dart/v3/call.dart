dynamic process({dynamic value, dynamic label}) => null;
final my_data = null;
void main() {
    process(value: "hello", label: "a");
    process(value: 42, label: "b");
    process(value: true, label: "c");
}
