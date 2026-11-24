#include <map>
#include <string>
int main() {
auto my_data = std::map<std::string, unsigned long long>{
    {"a", 0x7fffffffffffffff},
    {"b", 9223372036854775808ULL},
};
    (void)my_data;
    return 0;
}
