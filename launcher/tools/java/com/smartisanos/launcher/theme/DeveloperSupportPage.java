package com.smartisanos.launcher.theme;

import android.app.Activity;
import android.content.res.Resources;
import android.graphics.drawable.Drawable;
import android.util.Log;
import android.view.View;
import android.widget.ImageView;

import com.smartisanos.home.settings.icons.IconBitmapDecoder;
import com.smartisanos.launcher.theme.MaintainedLauncherSettingsHost.SettingsResourceContext;

import static com.smartisanos.launcher.theme.MaintainedLauncherSettingsHost.*;

/** Offline donation images, owned only by the visible settings page. */
final class DeveloperSupportPage implements View.OnAttachStateChangeListener {
    private final Resources resources;
    private final View root;
    private final Drawable[] images = new Drawable[2];
    private int selected = -1;

    private DeveloperSupportPage(Resources resources, View root) {
        this.resources = resources;
        this.root = root;
        root.addOnAttachStateChangeListener(this);
    }

    static void show(final Activity activity) {
        try {
            SettingsResourceContext context = createSettingsContext(activity);
            final Resources resources = context.getResources();
            final View root = inflate(activity, context, "setting_developer_support");
            final DeveloperSupportPage page = new DeveloperSupportPage(resources, root);
            bindBackTitle(activity, resources, root, "view_title", text(resources, "donate_title"),
                    "SUPPORT_DEVELOPER", new Runnable() {
                        public void run() { showAboutPage(activity, false); }
                    });
            click(activity, resources, root, "donate_wechat_option", new View.OnClickListener() {
                public void onClick(View view) { page.select(0); }
            });
            click(activity, resources, root, "donate_alipay_option", new View.OnClickListener() {
                public void onClick(View view) { page.select(1); }
            });
            page.select(0);
            setSettingsContentView(activity, context, resources, root, true);
        } catch (Exception error) {
            Log.w("DeveloperSupport", "Unable to open support page", error);
            Resources resources = getMaintainedResources(activity);
            showInfoDialog(activity, text(resources, "donate_title"), text(resources, "donate_page_error"));
        }
    }

    private void select(int method) {
        if (method == selected) return;
        selected = method;
        find(resources, root, "donate_wechat_checked").setVisibility(method == 0 ? View.VISIBLE : View.INVISIBLE);
        find(resources, root, "donate_alipay_checked").setVisibility(method == 1 ? View.VISIBLE : View.INVISIBLE);
        find(resources, root, "donate_wechat_option").setSelected(method == 0);
        find(resources, root, "donate_alipay_option").setSelected(method == 1);
        ImageView code = (ImageView) find(resources, root, "donate_code");
        View error = find(resources, root, "donate_image_error");
        code.setContentDescription(text(resources, method == 0 ? "donate_wechat_code" : "donate_alipay_code"));
        try {
            if (images[method] == null) {
                images[method] = IconBitmapDecoder.loadResourceDrawablePreservingPixels(resources,
                        drawable(resources, method == 0 ? "donate_wechat" : "donate_alipay"));
            }
            if (images[method] == null) throw new Resources.NotFoundException("Missing donation image");
            code.setImageDrawable(images[method]);
            code.setVisibility(View.VISIBLE);
            error.setVisibility(View.GONE);
        } catch (Resources.NotFoundException errorLoadingImage) {
            Log.w("DeveloperSupport", "Unable to load local donation image", errorLoadingImage);
            code.setImageDrawable(null);
            code.setVisibility(View.GONE);
            error.setVisibility(View.VISIBLE);
        }
    }

    public void onViewAttachedToWindow(View view) {
        if (((ImageView) find(resources, root, "donate_code")).getDrawable() == null) {
            int method = selected;
            selected = -1;
            select(method < 0 ? 0 : method);
        }
    }

    public void onViewDetachedFromWindow(View view) {
        ((ImageView) find(resources, root, "donate_code")).setImageDrawable(null);
        // Resource drawables may share bitmap ownership. Release references, never recycle them.
        images[0] = null;
        images[1] = null;
    }

    private static String text(Resources resources, String name) {
        return resources.getString(resources.getIdentifier(name, "string", SETTINGS_PKG));
    }
}
