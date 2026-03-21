@interface NSObject
+ (instancetype)alloc;
- (instancetype)init;
@end
@interface NSString : NSObject
@end
@interface NSArray : NSObject
+ (instancetype)arrayWithObjects:(const id [])objects count:(unsigned long)cnt;
@end
void _check(void) {
id my_data = @[
    @"foo",
    @"bar",
    @"baz",
];
    (void)my_data;
}
