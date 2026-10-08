#include <initializer_list>
#include <string>
#include <map>
int main() {
auto my_data = std::map<std::string, int>{
    {"not-a-field", 1},
};
    (void)my_data;
    return 0;
}
