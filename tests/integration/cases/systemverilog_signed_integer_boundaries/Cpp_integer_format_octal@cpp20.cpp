#include <initializer_list>
#include <string>
#include <map>
int main() {
auto my_data = std::map<std::string, long long>{
    {"i32_below", -020000000001LL},
    {"i32_minimum", -020000000000LL},
    {"i32_above", -017777777777},
    {"i32_maximum", 017777777777},
    {"i32_over", 020000000000},
    {"i64_minimum", (-9223372036854775807LL - 1)},
    {"i64_maximum", 0777777777777777777777},
};
    (void)my_data;
    return 0;
}
