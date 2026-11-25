#import <Foundation/Foundation.h>
static void f(id _a0) { (void)_a0; }
int main(void) {
@autoreleasepool {
id ref_data = @[
    @[
        @1,
        @2,
    ],
    @[
        @3,
        @4,
    ],
];
f(@[
    @[
        ref_data,
    ],
]);
}
    return 0;
}
