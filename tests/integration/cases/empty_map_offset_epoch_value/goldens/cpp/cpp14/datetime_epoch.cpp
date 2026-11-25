#include <map>
#include <string>
#include <vector>
int main() {
auto my_data = std::vector<std::map<std::string, long long>>{
    std::map<std::string, long long>{{"timestamp", 2208988800}},
    std::map<std::string, long long>{},
};
    (void)my_data;
    return 0;
}
