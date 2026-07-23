#include <initializer_list>
#include <string>
#include <map>
#include <vector>
int main() {
auto my_data = std::map<std::string, std::vector<std::string>>{
    {"vals", std::vector<std::string>{"2024-01-15", "09:30:00"}},
};
(void)my_data;
my_data = std::map<std::string, std::vector<std::string>>{
    {"vals", std::vector<std::string>{"2024-01-15", "09:30:00"}},
};
    (void)my_data;
    return 0;
}
