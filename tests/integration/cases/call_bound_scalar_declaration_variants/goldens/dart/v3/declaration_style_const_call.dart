dynamic consume({dynamic value}) => null;
final my_data = null;
void main() {
    const shared = 42;
    consume(value: shared);
}
