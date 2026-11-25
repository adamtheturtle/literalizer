#include <string>
struct Record0 { std::string event_date; std::string event_time; std::string event_datetime; };
int main() {
auto my_data = Record0{
    "2024-01-15",
    "12:30:00",
    "2024-01-15T12:30:00+00:00",
};
    (void)my_data;
    return 0;
}
