#include <initializer_list>
#include <string>
#include <map>
int main() {
auto my_data = std::map<std::string, long long>{
    {"i32_below", -2147483649},
    {"i32_minimum", -2147483648},
    {"i32_above", -2147483647},
    {"i32_maximum", 2147483647},
    {"i32_over", 2147483648},
    {"i64_minimum", (-9223372036854775807LL - 1)},
    {"i64_maximum", 9223372036854775807},
};
    (void)my_data;
    return 0;
}
