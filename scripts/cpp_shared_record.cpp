#include "record_data.hpp"

#include <iostream>

int main() {
#include "record_bindings.inc"
    const auto& mixed = declaring_data;
    const auto& strings = dependent_data;
    if (mixed.size() != 2 || strings.size() != 2) {
        std::cerr << "Unexpected shared-record row count\n";
        return 1;
    }
    using Attributes = std::map<std::string, LiteralizerRecordValue>;
    if (mixed[0].name != "row_1" || mixed[0].attributes != Attributes{
            {"colour", std::string("red")}, {"discounted", true}} ||
        mixed[1].name != "row_2" || mixed[1].attributes != Attributes{
            {"colour", std::string("blue")},
            {"size", std::string("large")}} ||
        strings[0].name != "row_3" ||
        strings[0].attributes != Attributes{
            {"colour", std::string("green")},
            {"size", std::string("small")}} ||
        strings[1].name != "row_4" ||
        strings[1].attributes != Attributes{
            {"colour", std::string("white")}}) {
        std::cerr << "Unexpected shared-record values\n";
        return 1;
    }
    std::cout << R"json({"ok": true})json";
    return 0;
}
