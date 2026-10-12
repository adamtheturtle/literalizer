#include <initializer_list>
#include <string>
#include <unordered_map>
int main() {
auto my_data = std::unordered_map<std::string, std::string>{
    {"event_date", "2024-01-15"},
    {"event_time", "12:30:00"},
    {"event_datetime", "2024-01-15T12:30:00+00:00"},
};
    (void)my_data;
    return 0;
}
