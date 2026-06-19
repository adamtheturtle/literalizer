dynamic store_item({dynamic key, dynamic value}) => null;
dynamic read_item({dynamic key}) => null;
final my_data = null;
void main() {
    store_item(key: 1, value: 10);
    read_item(key: 1);
}
