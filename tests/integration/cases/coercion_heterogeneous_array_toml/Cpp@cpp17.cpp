#include <initializer_list>
#include <string>
#include <map>
#include <vector>
int main() {
auto my_data = std::map<std::string, std::vector<double>>{
    {"_", std::vector<double>{1, 2.5, 3}},
};
    (void)my_data;
    return 0;
}
