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
    @"48656c6c6f",
];
    (void)my_data;
}
