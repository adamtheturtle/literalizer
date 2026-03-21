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
    @"apple",  // inline comment
    // before banana
    @"banana",
    // trailing
]];
    (void)my_data;
}
