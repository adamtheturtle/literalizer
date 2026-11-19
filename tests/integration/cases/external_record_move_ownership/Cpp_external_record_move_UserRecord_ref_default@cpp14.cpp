#include <utility>
#include <memory>
struct UserRecord { int value{}; std::unique_ptr<int> move_guard = nullptr; };
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
