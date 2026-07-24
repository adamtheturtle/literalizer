#include <initializer_list>
#include <string>
#include <map>
#include <vector>
#include <cstddef>
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
  std::shared_ptr<Holder> value_;
 public:
  DynamicValue() : value_(new TypedHolder<std::nullptr_t>(nullptr)) {}
  template <typename T> explicit DynamicValue(T value) : value_(new TypedHolder<T>(std::move(value))) {}
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
struct mgrType_ { template <typename... Args> void run(Args...) const {} };
struct appType_ { mgrType_ mgr; };
const appType_ app;
int main() {
app.mgr.run(std::map<std::string, DynamicValue>{{"type", DynamicValue{"create"}}, {"pr_id", DynamicValue{"pr_1"}}, {"draft", DynamicValue{true}}});
app.mgr.run(std::map<std::string, DynamicValue>{{"type", DynamicValue{"create"}}, {"pr_id", DynamicValue{"pr_2"}}});
    return 0;
}
