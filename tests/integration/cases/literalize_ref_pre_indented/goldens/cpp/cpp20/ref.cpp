#include <vector>
#include <utility>
#include <map>
#include <string>
int main() {
    auto shared = std::vector<int>{
        1,
        2,
    };
    auto my_data = std::map<std::string, std::vector<int>>{
        {"a", std::move(shared)},
    };
    (void)my_data;
    return 0;
}
