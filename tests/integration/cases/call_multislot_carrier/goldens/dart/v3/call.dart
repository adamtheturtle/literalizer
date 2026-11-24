dynamic process({dynamic value, dynamic extra}) => null;
final my_data = null;
void main() {
    process(value: 1, extra: "hello");
    process(value: "two", extra: false);
    process(value: 3.5, extra: null);
}
