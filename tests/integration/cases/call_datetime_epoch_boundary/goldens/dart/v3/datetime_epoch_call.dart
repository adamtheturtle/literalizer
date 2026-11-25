dynamic consume({dynamic value}) => null;
final my_data = null;
void main() {
    consume(value: -2147483649);
    consume(value: 2147483648);
}
