use std::{env, fs, str, path::{Path, PathBuf}};
use usvg;
use tiny_skia;
use resvg;
use json;

fn json_from_file(build_dir: &Path, name: &Path) -> json::JsonValue {
    let mut full_path = PathBuf::new();
    full_path.push(build_dir);
    full_path.push(name);

    let file_data = fs::read(full_path).unwrap();
    let json_string = str::from_utf8(&file_data).ok().unwrap();
    return json::parse(json_string).unwrap();
}

fn main() {
    // Maybe not the best way but :shrug:
    let exe_path = env::current_exe().ok().unwrap();
    let build_dir = exe_path
        .parent().unwrap()
        .parent().unwrap()
        .parent().unwrap();

    let icons = json_from_file(build_dir, Path::new("icons.json"));

    println!("{}", json::stringify_pretty(icons, 2));

    // let mut opt = usvg::Options::default();

    // // Get file's absolute directory.
    // opt.resources_dir = std::fs::canonicalize(&args[1]).ok().and_then(|p| p.parent().map(|p| p.to_path_buf()));

    // let svg_data = std::fs::read(&args[1]).unwrap();

    // let s = match str::from_utf8(&svg_data) {
    //     Ok(v) => v,
    //     Err(e) => panic!("Invalid UTF-8 sequence: {}", e),
    // };

    // // colorize the absolute hack way
    // let svg_data = s.replace("#000", "#aa9bc1");

    // let rtree = usvg::Tree::from_data(svg_data.as_bytes(), &opt.to_ref()).unwrap();

    // // TODO: render at 16, 32 (@2x suffix), and 48 (@3x suffix)
    // let pixmap_size = rtree.svg_node().size.to_screen_size();
    // let mut pixmap = tiny_skia::Pixmap::new(pixmap_size.width(), pixmap_size.height()).unwrap();
    // resvg::render(&rtree, usvg::FitTo::Original, pixmap.as_mut()).unwrap();
    // pixmap.save_png(&args[2]).unwrap();
}
