#include <initializer_list>
#include <string>
#include <map>
#include <vector>
int main() {
auto x = 0;
auto y = 0;
auto my_data = std::vector<std::map<std::string, std::string>>{
    x,
    y,
};
    (void)my_data;
    return 0;
}
