#include <initializer_list>
#include <string>
#include <map>
#include <utility>
#include <vector>
struct Record0 { std::vector<std::pair<std::string, std::nullptr_t>> a; int b{}; };
int main() {
auto my_data = Record0{
    std::vector<std::pair<std::string, std::nullptr_t>>{},
    1,
};
    (void)my_data;
    return 0;
}
