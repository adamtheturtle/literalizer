#include <map>
#include <string>
int main() {
auto my_data = std::map<std::string, int>{
    {"a\"b", 1},
};
(void)my_data;
my_data = std::map<std::string, int>{
    {"a\"b", 1},
};
    (void)my_data;
    return 0;
}
