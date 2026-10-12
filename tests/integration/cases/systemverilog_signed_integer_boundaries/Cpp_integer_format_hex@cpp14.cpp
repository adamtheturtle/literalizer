#include <initializer_list>
#include <string>
#include <map>
int main() {
auto my_data = std::map<std::string, long long>{
    {"i32_below", -0x80000001LL},
    {"i32_minimum", -0x80000000LL},
    {"i32_above", -0x7fffffff},
    {"i32_maximum", 0x7fffffff},
    {"i32_over", 0x80000000},
    {"i64_minimum", (-9223372036854775807LL - 1)},
    {"i64_maximum", 0x7fffffffffffffff},
};
    (void)my_data;
    return 0;
}
