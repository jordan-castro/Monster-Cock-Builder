use color_name::Color;
use image::{Rgb, Rgba};

/// Conversion from RGB to its closest name.
/// 
/// **Params**
/// - `rgb: (i32, i32, i32)` The rgb color.
/// 
/// **Returns**
/// - `String` The name of the color.
pub fn rgb_name(rgb: (i32, i32, i32)) -> String {
    let color = [rgb.0 as u8, rgb.1 as u8, rgb.2 as u8];
    let name = Color::similar(color);
    name
}

/// Convert a Hexedecimal color to its RGB equivalent.
/// 
/// **Params**
/// - `hex: &str` The hex color.
/// 
/// **Returns**
/// - `(i32, i32, i32)` The rgb color.
pub fn hex_to_rgb(hex: &str) -> (i32, i32, i32) {
    let hex = hex.trim_start_matches('#');
    let r = u8::from_str_radix(&hex[0..2], 16).unwrap();
    let g = u8::from_str_radix(&hex[2..4], 16).unwrap();
    let b = u8::from_str_radix(&hex[4..6], 16).unwrap();
    (r as i32, g as i32, b as i32)
}

/// Conversion from RGB to its sRGB equivalent.
/// 
/// **Params**
/// - `rgb: (i32, i32, i32)` The rgb color.
/// 
/// **Returns**
/// - `(f32, f32, f32)` The sRGB equivalent.
pub fn rgb_to_srgb(rgb: (i32, i32, i32)) -> (f32, f32, f32) {
    let r = rgb.0 as f32 / 255.0;
    let g = rgb.1 as f32 / 255.0;
    let b = rgb.2 as f32 / 255.0;
    let r = if r <= 0.03928 {
        r / 12.92
    } else {
        ((r + 0.055) / 1.055).powf(2.4)
    };
    let g = if g <= 0.03928 {
        g / 12.92
    } else {
        ((g + 0.055) / 1.055).powf(2.4)
    };
    let b = if b <= 0.03928 {
        b / 12.92
    } else {
        ((b + 0.055) / 1.055).powf(2.4)
    };
    (r, g, b)
}

/// 
/// Convert a (i32, i32, i32) color to a [u8; 3] color.
/// 
/// # Params
/// - `rgb: (i32, i32, i32)` The rgb color.
/// 
/// # Returns
/// - `Rgb([u8; 3])` The [u8; 3] color.
/// 
pub fn rgb_to_u8(rgb: (i32, i32, i32)) -> Rgb<u8> {
    Rgb([rgb.0 as u8, rgb.1 as u8, rgb.2 as u8])
}

///
/// Convert a (i32, i32, i32) color to a [u8; 4] color.
/// 
/// # Params
/// - `rgb: (i32, i32, i32)` The rgb color.
/// 
/// # Returns
/// - `[u8; 4]` The [u8; 4] color.
/// 
pub fn rgb_to_rgba_u8(rgb: (i32, i32, i32)) -> [u8; 4] {
    [rgb.0 as u8, rgb.1 as u8, rgb.2 as u8, 255]
}

/// 
/// Convert a [u8; 4] color to Rgba struct.
/// 
/// # Params
/// - `rgba: [u8; 4]` The [u8; 4] color.
/// 
/// # Returns
/// - `Rgba([u8; 4])` The Rgba struct.
/// 
pub fn rgba_u8_to_struct(rgba: [u8; 4]) -> Rgba<u8> {
    Rgba([rgba[0], rgba[1], rgba[2], rgba[3]])
}

///
/// Convert a rgba to rgb [u3; 8]
/// 
/// # Params
/// - `rgba: [u8; 4]` The rgba color.
/// 
/// # Returns
/// - `[u8; 3]` The [u8; 3] color.
/// 
pub fn rgba_to_rgb_u8(rgba: [u8; 4]) -> [u8; 3] {
    [rgba[0], rgba[1], rgba[2]]
}

/// 
/// Convert a [u3; 8] color to a (i32, i32, i32) color.
/// 
/// # Params
/// - `rgb: [u8; 3]` The [u8; 3] color.
/// 
/// # Returns
/// - `(i32, i32, i32)` The (i32, i32, i32) color.
///
pub fn rgb_u8_to_i32(rgb: [u8; 3]) -> (i32, i32, i32) {
    (rgb[0] as i32, rgb[1] as i32, rgb[2] as i32)
}