class Main {
static class ThingType_ { Object go(Object arg0, Object arg1, Object arg2) { return null; } }
static ThingType_ thing = new ThingType_();
    public static void main() {
thing.go(new Object[]{}, new int[]{1}, new Object[]{});
thing.go(new String[]{"text"}, new int[]{2}, new Object[]{});
thing.go(new Object[]{}, new String[]{"text"}, new Object[]{});
thing.go(new String[]{"text"}, new int[]{2}, new int[]{3});
    }
}
