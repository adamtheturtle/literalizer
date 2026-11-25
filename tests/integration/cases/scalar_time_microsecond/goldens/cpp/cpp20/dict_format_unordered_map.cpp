#include <string>
#include <unordered_map>
int main() {
auto my_data = std::unordered_map<std::string, std::string>{
    {"exact_millisecond", "09:30:15.123000"},
    {"sub_millisecond", "09:30:15.123456"},
};
    (void)my_data;
    return 0;
}
