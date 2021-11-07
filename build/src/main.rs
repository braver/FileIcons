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

    let colors = json_from_file(&build_dir, Path::new("colors.json"));
    let icons = json_from_file(&build_dir, Path::new("icons.json"));
    let sizes = json_from_file(&build_dir, Path::new("sizes.json"));

    for kvp in icons.entries() {
        let mut full_icon_path = PathBuf::new();
        full_icon_path.push(&build_dir);
        full_icon_path.push("assets");
        full_icon_path.push(format!("{}.svg", kvp.0));

        let svg_data = match std::fs::read(&full_icon_path) {
            Ok(v) => v,
            Err(e) => panic!("Failed to read icon file {} ({})", full_icon_path.display(), e),
        };

        let s = match str::from_utf8(&svg_data) {
            Ok(v) => v,
            Err(e) => panic!("Invalid UTF-8 sequence: {}", e),
        };

        // colorize the absolute hack way
        let color = &colors[kvp.1.as_str().unwrap()];
        let svg_data = s.replace("#000", color.as_str().unwrap());

        let opt = usvg::Options::default();
        let rtree = usvg::Tree::from_data(svg_data.as_bytes(), &opt.to_ref()).unwrap();

        for size_desc in sizes.members() {
            let size = size_desc["size"].as_u32().unwrap();
            let suffix = if size_desc["suffix"].is_string() {
                size_desc["suffix"].as_str().unwrap()
            } else {
                ""
            };

            let mut full_output_path = PathBuf::new();
            full_output_path.push(&theme_dir);
            full_output_path.push(format!("{}{}.png", kvp.0, suffix));

            println!("Building {} to {}", full_icon_path.display(), full_output_path.display());
            let mut pixmap = tiny_skia::Pixmap::new(size, size).unwrap();
            resvg::render(&rtree, usvg::FitTo::Size(size, size), pixmap.as_mut()).unwrap();

            pixmap.save_png(full_output_path).unwrap();
        }
    }
}
