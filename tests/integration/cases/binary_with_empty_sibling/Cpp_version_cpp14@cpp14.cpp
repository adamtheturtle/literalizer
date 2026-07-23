#include <initializer_list>
#include <string>
#include <vector>
#include <cstddef>
#include <memory>
#include <utility>
struct Value {
 private:
  struct Holder { virtual ~Holder() {} };
  template <typename T> struct TypedHolder : Holder {
    explicit TypedHolder(T value) : value(std::move(value)) {}
    T value;
  };
  std::shared_ptr<Holder> value_;
 public:
  Value() : value_(new TypedHolder<std::nullptr_t>(nullptr)) {}
  template <typename T> Value(T value) : value_(new TypedHolder<T>(std::move(value))) {}
  template <typename T> bool is() const {
    return dynamic_cast<TypedHolder<T>*>(value_.get()) != nullptr;
  }
  template <typename T> T& get() {
    return static_cast<TypedHolder<T>*>(value_.get())->value;
  } // get
  template <typename T> const T& get() const {
    return static_cast<const TypedHolder<T>*>(value_.get())->value;
  } // get const
};
int main() {
auto my_data = std::vector<Value>{
    "48656c6c6f",
    std::vector<std::nullptr_t>{},
};
    (void)my_data;
    return 0;
}
