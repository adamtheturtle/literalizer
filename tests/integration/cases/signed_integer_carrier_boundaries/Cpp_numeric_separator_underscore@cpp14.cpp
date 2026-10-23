#include <initializer_list>
#include <string>
#include <map>
int main() {
auto my_data = std::map<std::string, long long>{
    {"i32_below", -2'147'483'649},
    {"i32_minimum", (-2'147'483'647 - 1)},
    {"i32_above", -2'147'483'647},
    {"i32_maximum", 2'147'483'647},
    {"i32_over", 2'147'483'648},
    {"i64_minimum", (-9223372036854775807LL - 1)},
    {"i64_maximum", 9'223'372'036'854'775'807},
};
    (void)my_data;
    return 0;
}
