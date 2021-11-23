use image::{RgbImage, Rgba, imageops};

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

///
/// Crop a image to a specific size.
/// 
/// # Params
/// - `image: RgbImage` The image to crop.
/// 
/// # Returns
/// `RgbImage` The cropped image.
/// 
pub fn crop_image(image: RgbImage) -> RgbImage {
    let mut img = image.to_owned();
    let (width, height) = image.dimensions();
    let crop_width = width - 100;
    let crop_height = height - 100;
    img = imageops::crop(&mut img, 50, 50, crop_width - 50, crop_height - 50).to_image();
    img
}