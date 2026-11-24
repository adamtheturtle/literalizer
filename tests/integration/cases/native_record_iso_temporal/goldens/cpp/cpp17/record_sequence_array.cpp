#include <string>
struct Record0 { std::string birthday; std::string moment; std::string at; };
int main() {
auto my_data = Record0{
    "2024-01-15",
    "2024-01-15T12:30:00+00:00",
    "09:30:00",
};
    (void)my_data;
    return 0;
}
