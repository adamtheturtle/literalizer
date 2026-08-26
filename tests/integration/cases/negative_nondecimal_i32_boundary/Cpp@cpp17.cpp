#include <initializer_list>
#include <string>
#include <map>
int main() {
auto my_data = std::map<std::string, long long>{
    {"minimum", -2147483648},
    {"below", -3000000000},
};
    (void)my_data;
    return 0;
}
