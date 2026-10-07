#include <initializer_list>
#include <string>
#include <utility>
#include <vector>
int main() {
auto bound = 2;
auto my_data = std::vector<std::pair<std::string, int>>{
    {"value", bound},
};
    (void)my_data;
    return 0;
}
