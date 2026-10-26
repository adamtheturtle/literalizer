#include <string>
#include <unordered_map>
int main() {
auto my_data = std::unordered_map<std::string, std::string>{
    {"date", "0099-05-27"},
    {"naive", "0001-01-01T12:30:00"},
    {"recent", "2024-05-27T10:00:00"},
};
    (void)my_data;
    return 0;
}
