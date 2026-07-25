#include <initializer_list>
#include <string>
#include <map>
int main() {
auto my_data = std::map<std::string, std::map<std::string, int>>{
    {"metrics", std::map<std::string, int>{{"count", 100}, {"rate", 50}}},
    {"flags", std::map<std::string, int>{{"retries", 3}, {"timeout", 30}}},
};
    (void)my_data;
    return 0;
}
