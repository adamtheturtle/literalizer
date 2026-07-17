#include <initializer_list>
#include <string>
#include <map>
int main() {
auto my_data = std::map<std::string, long long>{
    {"a", 1},
    {"b", 1099511627776},
};
(void)my_data;
my_data = std::map<std::string, long long>{
    {"a", 1},
    {"b", 1099511627776},
};
    (void)my_data;
    return 0;
}
