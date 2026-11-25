#include <map>
#include <string>
int main() {
auto my_data = std::map<std::string, double>{
    {"a", 0b1},
    {"b", 2.5},
    {"c", 0b11},
};
    (void)my_data;
    return 0;
}
