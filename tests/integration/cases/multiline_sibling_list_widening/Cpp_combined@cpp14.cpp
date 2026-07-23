#include <initializer_list>
#include <string>
#include <map>
#include <vector>
#include <utility>
#include <cstddef>
#include <memory>
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
auto my_data = std::map<std::string, Value>{
    {"omap_value", std::vector<std::pair<std::string, int>>{{"first", 1}}},
    {"sibling_lists", std::map<std::string, Value>{{"numbers", std::vector<int>{1, 2}}, {"strings", std::vector<std::string>{"x", "y"}}}},
    {"ref_marker_present", std::vector<std::string>{"$keep", "z"}},
};
(void)my_data;
my_data = std::map<std::string, Value>{
    {"omap_value", std::vector<std::pair<std::string, int>>{{"first", 1}}},
    {"sibling_lists", std::map<std::string, Value>{{"numbers", std::vector<int>{1, 2}}, {"strings", std::vector<std::string>{"x", "y"}}}},
    {"ref_marker_present", std::vector<std::string>{"$keep", "z"}},
};
    (void)my_data;
    return 0;
}
