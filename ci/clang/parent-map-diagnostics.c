#include <stdbool.h>
#include <stddef.h>
typedef struct CVal CVal;
typedef struct CKV CKV;
struct CVal {
  union {
    _Bool b;
    long long i;
    unsigned long long u;
    double f;
    const char *s;
    const CVal *a;
    const CKV *m;
  };
};
struct CKV {
  const char *k;
  CVal v;
};
struct Padded {
  char first;
  int middle;
  char last;
};
int main(void) {
  struct Padded values[8];
  (void)values;
  CVal value = ((CVal){
      .a = (CVal[]){((CVal){
          .a = (CVal[]){((CVal){
              .a = (CVal[]){((CVal){
                  .a = (CVal[]){((CVal){
                      .a = (CVal[]){((CVal){
                          .a = (CVal[]){((CVal){.i = 1})}})}})}})}})}})}});
  (void)value;
  return sizeof(sizeof(int));
}
