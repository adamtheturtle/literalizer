#include <utility>
#include <memory>
struct UserRecord { int move_guard{}; std::unique_ptr<int> move_guardx = nullptr; };
struct Record0 { UserRecord child; };
template <typename... Args> auto consume_widget(Args...) { return 0; }
int main() {
auto first = Record0{
    {
        1,
    },
};
consume_widget(std::move(first));
    return 0;
}
