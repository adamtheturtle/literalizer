#include <vector>
#include <string>
struct Record0 { int due_date{}; int parent_id{}; std::string assignee; };
int main() {
auto my_data = std::vector{
    Record0{.due_date = -1, .parent_id = -1, .assignee = ""},
    Record0{.due_date = 10, .parent_id = 20, .assignee = "alice"},
};
    (void)my_data;
    return 0;
}
