dynamic consume({dynamic value}) => null;
final my_data = null;
void main() {
    final shared = 42;
    consume(value: shared);
}
