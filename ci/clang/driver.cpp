#include "llvm/Support/InitLLVM.h"
#include "llvm/Support/LLVMDriver.h"

int clang_main(int argc, char **argv, const llvm::ToolContext &context);

int main(int argc, char **argv) {
  llvm::InitLLVM initialization(argc, argv);
  return clang_main(argc, argv, {argv[0], nullptr, false});
}
