#include <initializer_list>
#include <string>
#include <cstddef>
#include <map>
#include <memory>
#include <utility>
struct DynamicValue {
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
  static std::shared_ptr<Holder> make_holder(const char* value) {
    return std::make_shared<TypedHolder<std::string>>(value);
  } // make_holder string
  template <typename T> static std::shared_ptr<Holder> make_holder(T value) {
    return std::make_shared<TypedHolder<T>>(std::move(value));
  } // make_holder generic
  std::shared_ptr<Holder> value_;
 public:
  DynamicValue() : value_(new TypedHolder<std::nullptr_t>(nullptr)) {}
  template <typename T> explicit DynamicValue(T value) : value_(make_holder(std::move(value))) {}
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
auto my_data = std::map<std::string, DynamicValue>{
    {"s", DynamicValue{"string"}},
    {"i", DynamicValue{1}},
    {"f", DynamicValue{1.5}},
    {"b", DynamicValue{true}},
    {"n", DynamicValue{nullptr}},
    {"d", DynamicValue{"2024-01-15"}},
    {"dt", DynamicValue{"2024-01-15T12:00:00"}},
    {"by", DynamicValue{"48656c6c6f"}},
};
    (void)my_data;
    return 0;
}
