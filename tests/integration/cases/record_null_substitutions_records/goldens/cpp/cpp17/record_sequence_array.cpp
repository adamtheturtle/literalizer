#include <vector>
#include <string>
struct Record0 { int due_date{}; int parent_id{}; std::string assignee; };
int main() {
auto my_data = std::vector{
    Record0{-1, -1, ""},
    Record0{10, 20, "alice"},
};
    (void)my_data;
    return 0;
}
