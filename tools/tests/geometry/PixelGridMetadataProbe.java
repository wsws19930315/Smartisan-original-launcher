package com.smartisanos.launcher.theme;

import com.smartisanos.smengine.Camera;
import com.smartisanos.smengine.Ra;
import java.lang.reflect.Field;
import java.lang.reflect.Method;
import java.util.Map;

/** Exercise the built helper with mutable geometry and inherited field owners. */
public final class PixelGridMetadataProbe {
    private static int checks;
    public static class Vector {
        public float x = 1, y = 1, z = 1;
    }
    public static class Parent {
        public Parent parent;
        public int animation;
        public final Vector scale = new Vector();
        public Parent getParent() { return parent; }
        public int getAnimationState() { return animation; }
        public Vector getScale() { return scale; }
    }
    public static class ItemBase { private int itemType; }
    public static class Item extends ItemBase {}
    public static class CellBase extends Parent {
        private Object Rj = new Item();
        private int fH = 20;
        private final Object[] sc = new Object[8];
    }
    public static class Cell extends CellBase {}
    public static class Node {
        public Object renderTarget;
        public int updates, projections;
        public float width = 100, height = 100;
        public final Vector position = new Vector();
        public Node() { position.x = 10.25f; position.y = 20.75f; }
        public Object getRenderTarget() { return renderTarget; }
        public String getTextureName(int slot) { return "icon"; }
        public String getTextureName(String slot) { throw new AssertionError("wrong texture overload"); }
        public void getCornerPointScreenCoord(Camera camera, float[] points) {
            projections++;
            points[0] = position.x; points[1] = position.y;
            points[3] = position.x + width; points[4] = position.y + height;
        }
        public void getCornerPointScreenCoord(Object camera, Object points) {
            throw new AssertionError("wrong corner overload");
        }
        public Vector getLocation() { return position; }
        public float getWidth() { return width; }
        public float getHeight() { return height; }
        public void setTranslate(float x, float y, float z) {
            position.x = x; position.y = y; position.z = z;
        }
        public void setTranslate(double x, double y, double z) {
            throw new AssertionError("wrong translate overload");
        }
        public void updateGeometricState() { updates++; }
    }
    private static void check(boolean value, String message) {
        checks++; if (!value) throw new AssertionError(message);
    }
    private static void equal(float actual, float expected, String message) {
        check(Float.floatToIntBits(actual) == Float.floatToIntBits(expected), message);
    }
    private static Field field(Class<?> type, String name) throws Exception {
        Field value = type.getDeclaredField(name); value.setAccessible(true); return value;
    }
    private static Cell cell(Node node, int mode) throws Exception {
        Cell cell = new Cell();
        field(CellBase.class, "fH").setInt(cell, mode);
        ((Object[]) field(CellBase.class, "sc").get(cell))[0] = node;
        return cell;
    }
    @SuppressWarnings("unchecked")
    private static void exercise() throws Exception {
        Node node = new Node(); Cell cell = cell(node, 20);
        LauncherSettingBridge.alignStaticIconPixelGrid(cell);
        equal(node.position.x, 10, "static x phase");
        equal(node.position.y, 21, "static y phase");
        equal(node.position.z, 1, "z unchanged");
        check(node.updates == 1, "one subpixel correction");
        Map<Class<?>, Map<String, Field>> fields = (Map<Class<?>, Map<String, Field>>)
                field(LauncherSettingBridge.class, "GEOMETRY_FIELDS").get(null);
        Map<Class<?>, Map<String, Method>> methods = (Map<Class<?>, Map<String, Method>>)
                field(LauncherSettingBridge.class, "PIXEL_GRID_METHODS").get(null);
        check(fields.containsKey(Cell.class) && fields.get(Cell.class).size() == 3,
                "inherited cell metadata reused");
        check(fields.get(Item.class).get("itemType").getDeclaringClass() == ItemBase.class,
                "inherited item owner retained");
        Method corner = methods.get(Node.class).get("getCornerPointScreenCoord:2");
        check(corner != null && corner.getParameterTypes()[0] == Camera.class,
                "exact corner signature cached");
        Method renderer = methods.get(Ra.class).get("getInstance:0");
        check(renderer != null, "renderer accessor cached");
        Field owner = fields.get(Cell.class).get("Rj");
        for (int i = 0; i < 1000; i++) LauncherSettingBridge.alignStaticIconPixelGrid(cell);
        check(node.updates == 1, "no cumulative position correction");
        check(owner == fields.get(Cell.class).get("Rj")
                && corner == methods.get(Node.class).get("getCornerPointScreenCoord:2")
                && renderer == methods.get(Ra.class).get("getInstance:0"),
                "metadata identity remains stable");
        // Metadata reuse must not freeze geometry, engine owners or guard results.
        for (int mode : new int[] {12, 20}) {
            Node dynamic = new Node(); Cell current = cell(dynamic, mode);
            Parent parent = new Parent(); current.parent = parent;
            parent.animation = 1; LauncherSettingBridge.alignStaticIconPixelGrid(current);
            check(dynamic.projections == 0, "animated ancestor skipped");
            parent.animation = 0; parent.scale.x = 2;
            LauncherSettingBridge.alignStaticIconPixelGrid(current);
            check(dynamic.projections == 0, "scaled ancestor skipped");
            parent.scale.x = 1; dynamic.renderTarget = new Object();
            LauncherSettingBridge.alignStaticIconPixelGrid(current);
            check(dynamic.projections == 0, "render target skipped");
            dynamic.renderTarget = null;
            Object[] nodes = (Object[]) field(CellBase.class, "sc").get(current);
            nodes[7] = new Object(); LauncherSettingBridge.alignStaticIconPixelGrid(current);
            check(dynamic.projections == 0, "active icon skipped"); nodes[7] = null;
            dynamic.width = 99; LauncherSettingBridge.alignStaticIconPixelGrid(current);
            check(dynamic.updates == 0, "non 1:1 texture skipped");
            dynamic.width = 100; LauncherSettingBridge.alignStaticIconPixelGrid(current);
            check(dynamic.updates == 1, "current mutable dimensions reread");
            dynamic.position.x = 30.75f;
            LauncherSettingBridge.alignStaticIconPixelGrid(current);
            equal(dynamic.position.x, 31, "new position reread");
            field(ItemBase.class, "itemType").setInt(field(CellBase.class, "Rj").get(current), 2);
            dynamic.position.x = 40.25f; LauncherSettingBridge.alignStaticIconPixelGrid(current);
            equal(dynamic.position.x, 40.25f, "new item type reread");
        }
        Node folder = new Node(); LauncherSettingBridge.alignStaticIconPixelGrid(cell(folder, 8));
        check(folder.projections == 0, "folder mode remains excluded");
        Cell empty = cell(null, 20); LauncherSettingBridge.alignStaticIconPixelGrid(empty);
        field(CellBase.class, "Rj").set(empty, null);
        LauncherSettingBridge.alignStaticIconPixelGrid(empty);
        check(fields.get(Cell.class).get("Rj") == owner, "null payload never replaces metadata");
        check(Ra.calls > 1000, "renderer instance queried each eligible draw");
        System.out.println("PASS PIXEL_GRID_METADATA checks=" + checks);
    }
    public static void main(String[] args) {
        try { exercise(); }
        catch (Throwable failure) { failure.printStackTrace(); System.exit(1); }
    }
}
