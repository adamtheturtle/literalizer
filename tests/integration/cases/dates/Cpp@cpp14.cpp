#include <initializer_list>
#include <string>
#include <map>
struct Record0 { std::string date; std::string datetime; };
int main() {
auto my_data = Record0{
    "2024-01-15",
    "2024-01-15T12:30:00+00:00",
};
    (void)my_data;
    return 0;
}
