#include <initializer_list>
#include <string>
#include <map>
int main() {
auto my_data = std::map<std::string, double>{
    {"value", 1.2345678901234567},
};
    (void)my_data;
    return 0;
}
