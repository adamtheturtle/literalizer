#include <initializer_list>
#include <string>
#include <vector>
#include <utility>
#include <variant>
struct Record0 { std::vector<std::pair<std::string, long long>> values; bool flag{}; std::vector<std::pair<std::string, std::vector<std::pair<std::string, long long>>>> nested_values; std::vector<std::pair<std::string, std::vector<long long>>> list_values; };
int main() {
auto my_data = Record0{
    {
        {"first", 2208988800},
    },
    true,
    {
        {"first", std::vector<std::pair<std::string, long long>>{
            {"nested", 2208988800},
        }},
    },
    {
        {"first", std::vector<long long>{
            2208988800,
        }},
    },
};
    (void)my_data;
    return 0;
}
