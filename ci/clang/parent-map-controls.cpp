#include "clang/AST/ASTContext.h"
#include "clang/AST/ParentMapContext.h"
#include "clang/AST/RecursiveASTVisitor.h"
#include "clang/ASTMatchers/ASTMatchFinder.h"
#include "clang/ASTMatchers/ASTMatchers.h"
#include "clang/Tooling/Tooling.h"
#include "llvm/Support/raw_ostream.h"
#include <algorithm>
#include <set>
#include <string>
#include <vector>
using namespace clang;
using namespace clang::ast_matchers;
std::string label(const DynTypedNode &N) {
  std::string Text;
  llvm::raw_string_ostream Out(Text);
  Out << N.getNodeKind().asStringRef() << ":"
      << N.getSourceRange().getBegin().getRawEncoding() << ":"
      << N.getSourceRange().getEnd().getRawEncoding();
  return Text;
}
struct Visitor : RecursiveASTVisitor<Visitor> {
  ASTContext &Context;
  std::set<std::string> Rows;
  unsigned MultipleParents = 0;
  Visitor(ASTContext &Context) : Context(Context) {}
  bool shouldVisitImplicitCode() const { return true; }
  bool shouldVisitTemplateInstantiations() const { return true; }
  template <class T> bool record(T &N) {
    auto Node = DynTypedNode::create(N);
    std::vector<std::string> Parents;
    for (const auto &P : Context.getParents(Node))
      Parents.push_back(label(P));
    std::sort(Parents.begin(), Parents.end());
    Parents.erase(std::unique(Parents.begin(), Parents.end()), Parents.end());
    if (Parents.size() > 1)
      ++MultipleParents;
    std::string Row = label(Node);
    for (const auto &P : Parents)
      Row += " " + P;
    Rows.insert(Row);
    return true;
  }
  bool VisitStmt(Stmt *S) { return record(*S); }
  bool VisitDecl(Decl *D) { return record(*D); }
  bool VisitTypeLoc(TypeLoc T) { return record(T); }
};
int main() {
  const std::vector<std::pair<std::string, std::string>> Cases = {{"c99", R"(
struct Item { union { long long i; const struct Item *a; }; };
void f(void) {
  struct Item data = {.a = (struct Item[]){
    {.a = (struct Item[]){{.a = (struct Item[]){{.i = 7}}}}}, {.i = 2}}};
  struct Padded { char first; int middle; char last; } local[8];
  (void)data; (void)local;
})"},
                                                                  {"c++14", R"(
template<class T> struct Box { void f() { if (true) {} } };
void g() { Box<int> box; box.f(); auto f = [] { return 1; }; (void)f(); }
namespace ns { struct T {}; }
void typed(ns::T) {}
)"},
                                                                  {"c++20", R"(
template<class T> int f(T t) { return t + 1; }
struct Value { int x = 1; };
void g() { int values[] = {f(1), f(2L)}; auto lambda = []<class T>(T t) {return t;}; (void)lambda(values); }
)"}};
  for (const auto &Case : Cases) {
    auto AST = tooling::buildASTFromCodeWithArgs(
        Case.second, {"-std=" + Case.first},
        Case.first == "c99" ? "control.c" : "control.cpp");
    if (!AST || AST->getDiagnostics().hasErrorOccurred())
      return 1;
    auto &Context = AST->getASTContext();
    Visitor V(Context);
    V.TraverseDecl(Context.getTranslationUnitDecl());
    llvm::outs() << "CASE " << Case.first << " ROWS " << V.Rows.size()
                 << " MULTIPLE " << V.MultipleParents << "\n";
    for (const auto &Row : V.Rows)
      llvm::outs() << Row << "\n";
    // Preserve matcher binding multiplicity, including successful descendant
    // matches below shared initializer expressions, and direct-child queries.
    llvm::outs() << "DESCENDANT "
                 << match(functionDecl(forEachDescendant(
                              integerLiteral().bind("value"))),
                          Context)
                        .size()
                 << "\n";
    std::set<std::string> ChildMatches;
    for (const auto &Result :
         match(initListExpr(has(expr())).bind("value"), Context))
      ChildMatches.insert(label(
          DynTypedNode::create(*Result.getNodeAs<InitListExpr>("value"))));
    llvm::outs() << "CHILD " << ChildMatches.size() << "\n";
    for (const auto &Row : ChildMatches)
      llvm::outs() << Row << "\n";
    llvm::outs() << "MISSING "
                 << match(functionDecl(forEachDescendant(callExpr(
                              callee(functionDecl(hasName("absent")))))),
                          Context)
                        .size()
                 << "\n";
  }
}
