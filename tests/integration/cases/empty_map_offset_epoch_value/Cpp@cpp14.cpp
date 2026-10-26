#include <map>
#include <string>
#include <vector>
int main() {
auto my_data = std::vector<std::map<std::string, std::string>>{
    std::map<std::string, std::string>{{"timestamp", "2040-01-01T03:00:00+03:00"}},
    std::map<std::string, std::string>{},
};
    (void)my_data;
    return 0;
}
