use crate::gen::attributes::cocktributes::CockTribute;
use crate::gen::colors::CockColors;
use crate::utils::rgb_conversions;
use image::{Rgb, RgbImage};

const CANVAS_PATH: &str = "data/art/canvas_large.png";
const CANVAS_WIDTH: u32 = 2000;
const CANVAS_HEIGHT: u32 = 2000;

/// The canvas "object" for the MonsterCock.
#[derive(Debug, Clone)]
pub struct Canvas {
    pub image: RgbImage,
    pub(super) train: bool,
}

impl Canvas {
    /// Create a new canvas object.
    ///
    /// # Params
    /// - `attributes: &Vec<CockTribute>` the attributes of the MonsterCock.
    /// - `cock_colors: &CockColors` The colors of the MonsterCock.
    /// - `light_base: bool` If the base of the canvas should start light.
    /// - `train: bool` If the canvas should be trained.
    pub fn new(light_base: bool, train: bool) -> Canvas {
        Canvas {
            image: {
                // Decide the color of the base. White or black
                let pixel = if light_base {
                    Rgb([255, 255, 255])
                } else {
                    Rgb([0, 0, 0])
                };

                RgbImage::from_pixel(CANVAS_WIDTH, CANVAS_HEIGHT, pixel)
            },
            train,
        }
    }

    /// Draw the canvas based on the attributes of the MonsterCock.
    ///
    /// # Params
    /// - `attributes: &Vec<CockTribute>` the attributes of the MonsterCock.
    pub fn draw_from_attributes(
        &mut self,
        cocktributes: Vec<CockTribute>,
        cock_colors: &mut CockColors,
    ) {
        // Check if there is a gradient
        let has_gradient = match cocktributes[2] {
            CockTribute::Gradient {
                vertical,
                horizontal,
            } => {
                if vertical || horizontal {
                    self.draw_gradient(vertical, cock_colors);
                    true
                } else {
                    false
                }
            }
            _ => false,
        };

        // Now draw the schemas
        match cocktributes[1] {
            CockTribute::Schema {
                circles,
                squares,
                stripes,
                round_squares,
            } => {
                if circles {
                    self.draw_circles();
                }
                if squares {
                    self.draw_squares();
                }
                if stripes {
                    self.draw_stripes();
                }
                // if round_squares {
                // self.draw_round_squares();
                // }
            }
            _ => {}
        };
        // Todo check if gradient still exists
    }

    /// Draw a gradient on a canvas.
    ///
    /// **Params:**
    /// - `vertical: bool` Is the gradient vertical or horizontal.
    ///
    /// **Returns:**
    /// - `RgbImage` La imagen del canvas con el gradiente.
    pub fn draw_gradient(&mut self, vertical: bool, cock_colors: &mut CockColors) {
        // The colors used in the gradient
        let start = rgb_conversions::rgb_to_u8(cock_colors.random_color_from_pallete());
        let stop = rgb_conversions::rgb_to_u8(cock_colors.random_color_from_pallete());

        if vertical {
            image::imageops::vertical_gradient(&mut self.image, &start, &stop);
        } else {
            image::imageops::horizontal_gradient(&mut self.image, &start, &stop);
        }
    }
}
