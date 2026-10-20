class Main {
static Object make_widget(Object arg0, Object arg1, Object arg2) { return null; }
    public static void main() {
make_widget(new Object[]{}, new int[]{1}, new Object[]{});
make_widget(new String[]{"text"}, new int[]{2}, new Object[]{});
make_widget(new Object[]{}, new String[]{"text"}, new Object[]{});
make_widget(new String[]{"text"}, new int[]{2}, new int[]{3});
    }
}
