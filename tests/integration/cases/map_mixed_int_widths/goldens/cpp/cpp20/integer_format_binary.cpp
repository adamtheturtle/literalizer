#include <map>
#include <string>
int main() {
auto my_data = std::map<std::string, long long>{
    {"a", 0b1},
    {"b", 0b10000000000000000000000000000000000000000},
};
    (void)my_data;
    return 0;
}
