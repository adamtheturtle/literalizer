dynamic record({dynamic value}) => null;
dynamic flush({dynamic count}) => null;
final my_data = null;
void main() {
    record(value: 42);
    flush(count: 3);
}
