#include <initializer_list>
#include <string>
#include <map>
int main() {
auto my_data = std::map<std::string, unsigned long long>{
    {"a", 9'223'372'036'854'775'807},
    {"b", 9223372036854775808ULL},
};
    (void)my_data;
    return 0;
}
