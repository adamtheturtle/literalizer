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
    // before apple
    @"apple",
    @"banana",  // banana inline
    // trailing
]];
    (void)_v;
}
