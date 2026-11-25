#include <map>
#include <string>
int main() {
auto my_data = std::map<std::string, int>{
    {"a-b", 1},
    {"a b", 2},
    {"a-b-2", 3},
};
    (void)my_data;
    return 0;
}
