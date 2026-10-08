#include <initializer_list>
#include <string>
#include <map>
int main() {
auto my_data = std::map<std::string, double>{
    {"f", 1.5},
    {"n", -3L},
};
    (void)my_data;
    return 0;
}
