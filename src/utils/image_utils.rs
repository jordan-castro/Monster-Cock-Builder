use image::{RgbImage, Rgba, imageops, Rgb};

use super::rgb_conversions::rgb_to_u8;

const DEFAULT_COCK: &str = "data/art/CockSepColors.png";

/// 
/// Make the Base cock image transparent.
/// 
pub fn make_transparent() {
    let mut image = image::open(DEFAULT_COCK).unwrap().to_rgba8();
    let white = Rgba([255, 255, 255, 255]);

    // Loop through all pixels and check if color is white 
    for pixel in image.pixels_mut() {
        if pixel == &white {
            // If white, make transparent
            pixel[3] = 0;
        }
    }
    image.save(DEFAULT_COCK).expect("Saving image as transparent.");
}

/// Crop a image to a specific size.
/// 
/// # Params
/// - `image: RgbImage` The image to crop.
/// 
/// # Returns
/// `RgbImage` The cropped image.
/// 
pub fn crop_image(image: RgbImage, coordinates: Option<(u32, u32, u32, u32)>) -> RgbImage {
    let mut img = image.to_owned();
    let (width, height) = image.dimensions();
    let crop_width = width - 100;
    let crop_height = height - 100;
    let (x, y, w, h) = match coordinates {
        Some(coordinates) => coordinates,
        None => (50, 50, crop_width, crop_height),
    };

    img = imageops::crop(&mut img, x, y, w, h).to_image();
    img
}

/// Draw a gradient on a image.
/// 
/// # Params
/// - `image: RgbImage` The image to draw the gradient on.
/// - `start: (i32, i32, i32)` The start color of the gradient.
/// - `end: (i32, i32, i32)` The end color of the gradient.
/// - `vertical: bool` If the gradient should be vertical or horizontal.
pub fn draw_gradient(image: RgbImage, start: (i32, i32, i32), end: (i32, i32, i32), vertical: bool) -> RgbImage {
    let start = &rgb_to_u8(start);
    let end = &rgb_to_u8(end);
    let mut image = image;

    if vertical {
        imageops::vertical_gradient(&mut image, start, end);
    } else {
        imageops::horizontal_gradient(&mut image, start, end);
    }

    image
}

/// Edit the pixels of a image.
/// 
/// # Params
/// - `image: RgbImage` The image to edit.
/// - `pre` The previous color of the pixel.
/// - `post` The new color of the pixel.
pub fn change_pixels(image: &mut RgbImage, pre: Vec<Rgb<u8>>, post: Vec<Rgb<u8>>) {
    // Loop through all pixels and check them with pre
    for pixel in image.pixels_mut() {
        for (i, color) in pre.iter().enumerate() {
            // If we get a hit, then swap it with post.
            if pixel == color {
                *pixel = post[i];
            }
        }
    }
}