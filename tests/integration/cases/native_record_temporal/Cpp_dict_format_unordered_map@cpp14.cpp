#include <string>
#include <unordered_map>
int main() {
auto my_data = std::unordered_map<std::string, std::string>{
    {"birthday", "2024-01-15"},
    {"meeting", "09:30:00"},
    {"event_time", "2024-01-15T12:30:00+00:00"},
};
    (void)my_data;
    return 0;
}
