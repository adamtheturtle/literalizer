dynamic process({dynamic data, dynamic count}) => null;
final my_data = null;
void main() {
    final shared = 1;
    final other = 2;
    process(data: shared, count: 1);
    process(data: other, count: 0);
    process(data: shared, count: 8);
}
