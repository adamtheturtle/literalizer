dynamic process({dynamic a, dynamic b}) => null;
final my_data = null;
void main() {
    final big_list = <String>[
        "x",
    ];
    process(a: <String, List<String>>{"k": big_list}, b: {"m": big_list});
}
