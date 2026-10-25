#include <initializer_list>
#include <string>
#include <map>
int main() {
auto my_data = std::map<std::string, int>{
    {"x", 1},
};
    (void)my_data;
    return 0;
}
