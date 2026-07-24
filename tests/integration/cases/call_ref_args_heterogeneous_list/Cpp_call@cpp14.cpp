#include <initializer_list>
#include <vector>
#include <string>
#include <cstddef>
#include <memory>
#include <utility>
struct Value {
 private:
  struct Holder {
    Holder() = default;
    Holder(const Holder&) = delete;
    Holder(Holder&&) = delete;
    Holder& operator=(const Holder&) = delete;
    Holder& operator=(Holder&&) = delete;
    virtual ~Holder() = default;
  };
  template <typename T> struct TypedHolder : Holder {
    explicit TypedHolder(T value) : value_(std::move(value)) {}
    T& get() { return value_; }
    const T& get() const { return value_; } // NOLINT(modernize-use-nodiscard)
   private:
    T value_;
  }; // TypedHolder
  std::shared_ptr<Holder> value_;
 public:
  Value() : value_(new TypedHolder<std::nullptr_t>(nullptr)) {}
  // NOLINTNEXTLINE(google-explicit-constructor,hicpp-explicit-conversions)
  template <typename T> Value(T value) : value_(new TypedHolder<T>(std::move(value))) {}
  template <typename T> bool is() const { // NOLINT(modernize-use-nodiscard)
    return dynamic_cast<TypedHolder<T>*>(value_.get()) != nullptr;
  }
  template <typename T> T& get() {
    return static_cast<TypedHolder<T>*>(value_.get())->get();
  } // get
  template <typename T> const T& get() const {
    return static_cast<const TypedHolder<T>*>(value_.get())->get();
  } // get const
};
template <typename... Args> auto process(Args...) { return 0; }
int main() {
auto my_ints = std::vector<int>{
    1,
    2,
    3,
};
auto my_strings = std::vector<std::string>{
    "a",
    "b",
};
auto my_empty = std::vector<std::nullptr_t>{};
process(std::move(my_ints), 42);
process(std::move(my_strings), 7);
process(std::move(my_empty), 99);
    return 0;
}
