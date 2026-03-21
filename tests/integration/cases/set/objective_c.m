@interface NSObject
+ (instancetype)alloc;
- (instancetype)init;
@end
@interface NSString : NSObject
@end
@interface NSArray : NSObject
+ (instancetype)arrayWithObjects:(const id [])objects count:(unsigned long)cnt;
@end
@interface NSSet : NSObject
+ (instancetype)set;
+ (instancetype)setWithArray:(NSArray *)array;
@end
void _check(void) {
    id _v = [NSSet setWithArray:@[
    @"apple",
    @"banana",
    @"cherry",
]];
    (void)_v;
}
