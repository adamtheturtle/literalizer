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
id my_data = [NSSet setWithArray:@[
    // before apple
    @"apple",
    @"banana",  // banana inline
    // trailing
]];
    (void)my_data;
}
