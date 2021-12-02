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
    pub cock_colors: CockColors,
    pub cocktributes: Vec<CockTribute>,
    pub (super) train: bool,
}

impl Canvas {
    /// Create a new canvas object.
    ///
    /// # Params
    /// - `attributes: &Vec<CockTribute>` the attributes of the MonsterCock.
    /// - `cock_colors: &CockColors` The colors of the MonsterCock.
    /// - `light_base: bool` If the base of the canvas should start light.
    /// - `train: bool` If the canvas should be trained.
    pub fn new(attributes: Vec<CockTribute>, cock_colors: CockColors, light_base: bool, train: bool) -> Canvas {
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
            cock_colors: cock_colors,
            cocktributes: attributes,
            train,
        }
    }

    /// Draw the canvas.
    pub fn draw_canvas(&mut self) {
        // Whether or not the canvas will have a gradient
        let has_gradient = match self.cocktributes[2] {
            CockTribute::Gradient {
                vertical,
                horizontal,
            } => {
                if vertical || horizontal {
                    println!("We are drawing a Gradient");
                    self.draw_gradient(vertical);
                    true
                } else {
                    false
                }
            }
            _ => false,
        };

        // Draw schemas
        self.draw_schemas();
    }

    /// Draw a gradient on a canvas.
    ///
    /// **Params:**
    /// - `vertical: bool` Is the gradient vertical or horizontal.
    ///
    /// **Returns:**
    /// - `RgbImage` La imagen del canvas con el gradiente.
    fn draw_gradient(&mut self, vertical: bool) {
        // The colors used in the gradient
        let start =
            rgb_conversions::rgb_to_u8(self.cock_colors.random_color_from_pallete());
        let stop =
            rgb_conversions::rgb_to_u8(self.cock_colors.random_color_from_pallete());

        if vertical {
            image::imageops::vertical_gradient(&mut self.image, &start, &stop);
        } else {
            image::imageops::horizontal_gradient(&mut self.image, &start, &stop);
        }
    }

    /// Draw the schemas on the canvas.
    pub (crate) fn draw_schemas(&mut self) {
        // Match for the schemas does not return anything
        match self.cocktributes[1] {
            CockTribute::Schema {
                circles,
                squares,
                stripes,
                round_squares, // Todo the round squares
            } => {
                // Draw the schemas
                if circles {
                    self.draw_circles();
                }
                if squares {
                    self.draw_squares();
                }
                if stripes {
                    self.draw_stripes();
                }
            }
            _ => {}
        }
    }
}
