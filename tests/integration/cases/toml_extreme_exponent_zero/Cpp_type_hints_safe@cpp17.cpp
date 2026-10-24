#include <initializer_list>
#include <string>
#include <map>
int main() {
auto my_data = std::map<std::string, double>{
    {"value", 0.0},
};
    (void)my_data;
    return 0;
}
