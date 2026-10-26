#include <map>
#include <string>
#include <vector>
int main() {
auto my_data = std::vector<std::map<std::string, std::map<std::string, std::vector<long long>>>>{
    std::map<std::string, std::map<std::string, std::vector<long long>>>{{"nested", std::map<std::string, std::vector<long long>>{{"times", std::vector<long long>{-2208988800}}}}},
    std::map<std::string, std::map<std::string, std::vector<long long>>>{},
};
    (void)my_data;
    return 0;
}
