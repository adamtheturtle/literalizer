#include <map>
#include <string>
int main() {
auto my_data = std::map<std::string, unsigned long long>{
    {"a", 0b111111111111111111111111111111111111111111111111111111111111111},
    {"b", 9223372036854775808ULL},
};
    (void)my_data;
    return 0;
}
