@interface NSObject
+ (instancetype)alloc;
- (instancetype)init;
@end
@interface NSArray : NSObject
+ (instancetype)arrayWithObjects:(const id [])objects count:(unsigned long)cnt;
@end
void _check(void) {
id my_data = @[
    @[],
    @[],
];
    (void)my_data;
}
