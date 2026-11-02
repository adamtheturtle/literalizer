#include "clang-tidy/utils/ExceptionAnalyzer.h"
#include "clang/Tooling/Tooling.h"
#include "llvm/Support/raw_ostream.h"
#include <algorithm>
#include <string>
#include <utility>
#include <vector>

using namespace clang;
using clang::tidy::utils::ExceptionAnalyzer;

void print(const ExceptionAnalyzer::ExceptionInfo &Info) {
  llvm::outs() << "state=" << static_cast<int>(Info.getBehaviour())
               << " unknown=" << Info.containsUnknownElements() << "\n";
  std::vector<std::string> Rows;
  for (const auto &Entry : Info.getExceptions()) {
    std::string Row =
        Entry.first ? QualType(Entry.first, 0).getAsString() : "<unknown>";
    Row += " @" + std::to_string(Entry.second.Loc.getRawEncoding());
    for (const auto &Frame : Entry.second.Stack)
      Row += " " + Frame.first->getQualifiedNameAsString() + "@" +
             std::to_string(Frame.second.getRawEncoding());
    Rows.push_back(std::move(Row));
  }
  std::sort(Rows.begin(), Rows.end());
  for (const auto &Row : Rows)
    llvm::outs() << Row << "\n";
}

int main() {
  const std::vector<std::string> Cases = {
      // A closed recursive component can be reused by independent callers.
      R"(
void cycle_a();
void cycle_b() { cycle_a(); }
void cycle_a() { cycle_b(); throw 1; }
void test_escape() noexcept {
  try { cycle_a(); } catch (int) {}
  cycle_b();
}
void test_caught() noexcept {
  try { cycle_a(); cycle_b(); } catch (int) {}
}
)",
      // A cached component must be traversed again when one of its callees
      // is already active. enter_b preserves the forward declaration identity.
      R"(
void a();
void b();
void enter_b() { b(); }
void a() { b(); }
void b() {
  try { a(); } catch (double) { throw 1; }
  throw 2.0;
}
void test_context() noexcept {
  try { a(); } catch (...) {}
  enter_b();
}
void test_caught() noexcept {
  try { a(); } catch (...) {}
  try { enter_b(); } catch (double) {}
}
)",
      // The same function can rethrow different exceptions in different
      // catches.
      R"(
void rethrow_current() { throw; }
void test_context() noexcept {
  try { throw 1; } catch (int) {
    try { rethrow_current(); } catch (int) {}
  }
  try { throw 2.0; } catch (double) { rethrow_current(); }
}
void test_caught() noexcept {
  try { throw 1; } catch (int) {
    try { rethrow_current(); } catch (int) {}
  }
}
)",
      // Constructors, captures, and unknown/noexcept declarations retain their
      // exception specifications under both optional analyzer assumptions.
      R"(
void unknown();
void no_throw() noexcept;
struct Item { Item() { throw 1; } };
struct Owner { Item value; Owner() : value() {} };
Item make_item() { return Item(); }
void test_constructor() noexcept { Owner value; }
void test_capture() noexcept { auto value = [item = make_item()] {}; }
void test_unknown() noexcept { unknown(); no_throw(); }
void test_decl_unknown();
void test_decl_noexcept() noexcept;
)",
      // Repeated calls above a recursive leaf remain tractable at small depth
      // in the stock control, while the separate stress case exercises
      // depth 30.
      R"(
void cycle() { cycle(); throw 1; }
template<int N> void repeated() {
  repeated<N - 1>(); repeated<N - 1>();
}
template<> void repeated<0>() { cycle(); }
void test_escape() noexcept { repeated<6>(); }
void test_caught() noexcept { try { repeated<6>(); } catch (int) {} }
)"};

  for (const auto *Standard : {"c++14", "c++17", "c++20"}) {
    for (unsigned Index = 0; Index < Cases.size(); ++Index) {
      auto AST = tooling::buildASTFromCodeWithArgs(
          Cases[Index], {std::string("-std=") + Standard, "-fexceptions"},
          "control.cpp");
      if (!AST || AST->getDiagnostics().hasErrorOccurred())
        return 1;
      unsigned Roots = 0;
      for (auto *D : AST->getASTContext().getTranslationUnitDecl()->decls()) {
        const auto *F = llvm::dyn_cast<FunctionDecl>(D);
        if (!F || F->getNameAsString().rfind("test_", 0) != 0)
          continue;
        ++Roots;
        for (unsigned Assumptions = 0; Assumptions < 4; ++Assumptions) {
          for (bool Body : {false, true}) {
            if (Body && !F->hasBody())
              continue;
            ExceptionAnalyzer Analyzer;
            Analyzer.ignoreBadAlloc(false);
            Analyzer.assumeUnannotatedFunctionsAsThrowing(Assumptions & 1);
            Analyzer.assumeMissingDefinitionsFunctionsAsThrowing(Assumptions &
                                                                 2);
            llvm::outs() << Standard << " case=" << Index << " "
                         << F->getNameAsString()
                         << " assumptions=" << Assumptions << " body=" << Body
                         << " ";
            print(Body ? Analyzer.analyze(F->getBody()) : Analyzer.analyze(F));
          }
        }
      }
      if (!Roots)
        return 2;
    }
  }
}
