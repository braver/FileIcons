use std::str;
use usvg;
use tiny_skia;
use resvg;

fn main() {
    let args: Vec<String> = std::env::args().collect();
    if args.len() != 3 {
        println!("Usage:\n\tminimal <in-svg> <out-png>");
        return;
    }

    let mut opt = usvg::Options::default();

    // Get file's absolute directory.
    opt.resources_dir = std::fs::canonicalize(&args[1]).ok().and_then(|p| p.parent().map(|p| p.to_path_buf()));

    let svg_data = std::fs::read(&args[1]).unwrap();

    let s = match str::from_utf8(&svg_data) {
        Ok(v) => v,
        Err(e) => panic!("Invalid UTF-8 sequence: {}", e),
    };

    // colorize the absolute hack way
    let svg_data = s.replace("#000", "#aa9bc1");

    let rtree = usvg::Tree::from_data(svg_data.as_bytes(), &opt.to_ref()).unwrap();

    // TODO: render at 16, 32 (@2x suffix), and 48 (@3x suffix)
    let pixmap_size = rtree.svg_node().size.to_screen_size();
    let mut pixmap = tiny_skia::Pixmap::new(pixmap_size.width(), pixmap_size.height()).unwrap();
    resvg::render(&rtree, usvg::FitTo::Original, pixmap.as_mut()).unwrap();
    pixmap.save_png(&args[2]).unwrap();
}
