use std::{env, fs, str, path::{Path, PathBuf}};
use usvg;
use tiny_skia;
use resvg;
use json;

fn build_dir() -> PathBuf {
    let exe_path = env::current_exe().ok().unwrap();
    return exe_path
        .parent().unwrap()
        .parent().unwrap()
        .parent().unwrap()
        .to_path_buf();
}

fn theme_dir() -> PathBuf {
    let exe_path = env::current_exe().ok().unwrap();
    let mut path = exe_path
        .parent().unwrap()
        .parent().unwrap()
        .parent().unwrap()
        .parent().unwrap()
        .to_path_buf();
    path.push("theme");
    return path;
}

fn json_from_file(build_dir: &Path, name: &Path) -> json::JsonValue {
    let mut full_path = PathBuf::new();
    full_path.push(build_dir);
    full_path.push(name);

    let file_data = fs::read(full_path).unwrap();
    let json_string = str::from_utf8(&file_data).ok().unwrap();
    return json::parse(json_string).unwrap();
}

fn main() {
    let build_dir = build_dir();
    let theme_dir = theme_dir();

    let _colors = json_from_file(&build_dir, Path::new("colors.json"));
    let icons = json_from_file(&build_dir, Path::new("icons.json"));
    let _sizes = json_from_file(&build_dir, Path::new("sizes.json"));

    for kvp in icons.entries() {
        let mut full_icon_path = PathBuf::new();
        full_icon_path.push(&build_dir);
        full_icon_path.push("assets");
        full_icon_path.push(format!("{}.svg", kvp.0));

        let mut full_output_path = PathBuf::new();
        full_output_path.push(&theme_dir);
        full_output_path.push(format!("{}.png", kvp.0));

        println!("Building {} to {}", full_icon_path.display(), full_output_path.display());

        let svg_data = match std::fs::read(&full_icon_path) {
            Ok(v) => v,
            Err(e) => panic!("Failed to read icon file {} ({})", full_icon_path.display(), e),
        };

        let s = match str::from_utf8(&svg_data) {
            Ok(v) => v,
            Err(e) => panic!("Invalid UTF-8 sequence: {}", e),
        };

        // colorize the absolute hack way
        let svg_data = s.replace("#000", "#aa9bc1");

        let opt = usvg::Options::default();
        let rtree = usvg::Tree::from_data(svg_data.as_bytes(), &opt.to_ref()).unwrap();

        // TODO: render at 16, 32 (@2x suffix), and 48 (@3x suffix)
        let pixmap_size = rtree.svg_node().size.to_screen_size();
        let mut pixmap = tiny_skia::Pixmap::new(pixmap_size.width(), pixmap_size.height()).unwrap();
        resvg::render(&rtree, usvg::FitTo::Original, pixmap.as_mut()).unwrap();

        pixmap.save_png(full_output_path).unwrap();
    }
}
