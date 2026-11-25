#include <map>
#include <string>
int main() {
auto my_data = std::map<std::string, std::string>{
    {"reference", "whole"},
};
(void)my_data;
my_data = std::map<std::string, std::string>{
    {"reference", "whole"},
};
    (void)my_data;
    return 0;
}
