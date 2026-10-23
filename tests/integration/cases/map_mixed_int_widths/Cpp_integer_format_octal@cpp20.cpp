#include <initializer_list>
#include <string>
#include <map>
int main() {
auto my_data = std::map<std::string, long long>{
    {"a", 01},
    {"b", 020000000000000},
};
    (void)my_data;
    return 0;
}
