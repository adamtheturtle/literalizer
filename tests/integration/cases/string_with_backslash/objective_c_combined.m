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
    @"C:\\path\\to\\file",
    @"back\\\\slash",
    @"hello \\\"world\\\"",
];
my_data = @[
    @"C:\\path\\to\\file",
    @"back\\\\slash",
    @"hello \\\"world\\\"",
];
    (void)my_data;
}
