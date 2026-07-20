#include <initializer_list>
#include <string>
#include <map>
template <typename... Types> struct LiteralizerVariant { template <typename T> LiteralizerVariant(T&&) {} };
int main() {
auto my_data = std::map<std::string, std::string>{
    {"date", "2024-01-15"},
    {"datetime", "2024-01-15T12:30:00+00:00"},
};
(void)my_data;
my_data = std::map<std::string, std::string>{
    {"date", "2024-01-15"},
    {"datetime", "2024-01-15T12:30:00+00:00"},
};
    (void)my_data;
    return 0;
}
