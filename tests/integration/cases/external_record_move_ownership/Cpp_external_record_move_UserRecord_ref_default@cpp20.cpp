#include <utility>
#include <memory>
struct UserRecord { int move_guard{}; std::unique_ptr<int> move_guardx = nullptr; };
struct Record0 { UserRecord child; };
auto consume_widget(auto...) { return 0; }
int main() {
auto first = Record0{
    .child = {
        .move_guard = 1,
    },
};
consume_widget(std::move(first));
    return 0;
}
