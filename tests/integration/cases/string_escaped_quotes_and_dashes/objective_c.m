@interface NSObject
+ (instancetype)alloc;
- (instancetype)init;
@end
@interface NSString : NSObject
@end
void _check(void) {
    id _v = @"hello \"world\" -- not a comment";
    (void)_v;
}
