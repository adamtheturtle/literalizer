#include <initializer_list>
#include <string>
#include <map>
#include <vector>
#include <utility>
#include <cstddef>
#include <memory>
struct CustomValue {
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
  CustomValue() : value_(new TypedHolder<std::nullptr_t>(nullptr)) {}
  template <typename T> explicit CustomValue(T value) : value_(new TypedHolder<T>(std::move(value))) {}
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
int main() {
auto my_data = std::map<std::string, CustomValue>{
    {"omap_value", CustomValue{std::vector<std::pair<std::string, int>>{{"first", 1}}}},
    {"sibling_lists", CustomValue{std::map<std::string, CustomValue>{{"numbers", CustomValue{std::vector<int>{1, 2}}}, {"strings", CustomValue{std::vector<std::string>{"x", "y"}}}}}},
    {"ref_marker_present", CustomValue{std::vector<std::string>{"$keep", "z"}}},
};
    (void)my_data;
    return 0;
}
