#include <initializer_list>
#include <string>
#include <cstddef>
#include <map>
#include <memory>
#include <utility>
struct TaskValue {
 private:
  struct Holder { virtual ~Holder() {} };
  template <typename T> struct TypedHolder : Holder {
    explicit TypedHolder(T value) : value(std::move(value)) {}
    T value;
  };
  std::shared_ptr<Holder> value_;
 public:
  TaskValue() : value_(new TypedHolder<std::nullptr_t>(nullptr)) {}
  template <typename T> TaskValue(T value) : value_(new TypedHolder<T>(std::move(value))) {}
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
auto my_data = std::map<std::string, std::map<std::string, TaskValue>>{
    {"outer", std::map<std::string, TaskValue>{{"a", 1}, {"b", "x"}, {"c", nullptr}}},
};
    (void)my_data;
    return 0;
}
