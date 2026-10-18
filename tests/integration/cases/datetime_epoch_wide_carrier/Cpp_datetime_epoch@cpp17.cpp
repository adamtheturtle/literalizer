#include <initializer_list>
#include <string>
#include <map>
int main() {
auto my_data = std::map<std::string, long long>{
    {"within_i32", 1705320000},
    {"beyond_i32", 4085195400},
};
    (void)my_data;
    return 0;
}
