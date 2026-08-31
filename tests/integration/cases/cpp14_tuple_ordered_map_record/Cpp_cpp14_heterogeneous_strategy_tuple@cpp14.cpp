#include <initializer_list>
#include <string>
#include <vector>
#include <utility>
struct Record0 { int id{}; };
int main() {
auto my_data = std::vector<std::pair<std::string, std::vector<Record0>>>{
    {"entries", std::vector<Record0>{Record0{1}}},
};
    (void)my_data;
    return 0;
}
