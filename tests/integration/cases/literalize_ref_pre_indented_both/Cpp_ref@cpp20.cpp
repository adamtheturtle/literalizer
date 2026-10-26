#include <vector>
#include <map>
#include <string>
int main() {
        auto shared = std::vector<int>{
            1,
            2,
        };
        auto my_data = std::map<std::string, std::vector<int>>{
            {"a", shared},
        };
(void)my_data;
        my_data = std::map<std::string, std::vector<int>>{
            {"a", shared},
        };
    (void)my_data;
    return 0;
}
