use crate::gen::colors::CockColors;
use crate::{gen::attributes::cocktributes::CockTribute, utils::image_utils};
use image::{imageops, Rgb, RgbImage};

const CANVAS_PATH: &str = "data/art/canvas_large.png";
const CANVAS_WIDTH: u32 = 2000;
const CANVAS_HEIGHT: u32 = 2000;

/// The canvas "object" for the MonsterCock.
#[derive(Debug, Clone)]
pub struct Canvas {
    pub image: RgbImage,
    pub(super) train: bool,
    light_base: bool,
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
            light_base,
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
        let mut has_gradient = false;
        for attribute in cocktributes {
            match attribute {
                CockTribute::GradientVertical => {
                    has_gradient = true;
                    self.draw_gradient(true, cock_colors);
                }
                CockTribute::GradientHorizontal => {
                    has_gradient = true;
                    self.draw_gradient(false, cock_colors);
                }
                CockTribute::SchemaCircles => {
                    self.draw_circles();
                }
                CockTribute::SchemaStripes => {
                    self.draw_stripes();
                }
                CockTribute::SchemaSquares => {
                    self.draw_squares();
                }
                CockTribute::SchemaRoundSquares => todo!(),
                CockTribute::SchemaSpace => {
                    self.draw_space();
                }
                CockTribute::SchemaGSquares => {
                    self.draw_squares_with_gradients();
                }
                _ => {}
            };
        }
        // Todo check if gradient still exists
        self.resize();
    }

    /// Draw a gradient on a canvas.
    ///
    /// **Params:**
    /// - `vertical: bool` Is the gradient vertical or horizontal.
    ///
    /// **Returns:**
    /// - `RgbImage` La imagen del canvas con el gradiente.
    pub fn draw_gradient(&mut self, vertical: bool, cock_colors: &mut CockColors) {
        self.image = image_utils::draw_gradient(
            self.image.clone(),
            cock_colors.random_color_from_pallete(),
            cock_colors.random_color_from_pallete(),
            vertical,
        )
    }

    /// Clear the canvas.
    /// This is used when training the schemas verifier model.
    pub(crate) fn clear(&mut self) {
        // Reset the image to blank.
        // Decide the color of the base. White or black
        self.image = {
            let pixel = if self.light_base {
                Rgb([255, 255, 255])
            } else {
                Rgb([0, 0, 0])
            };

            RgbImage::from_pixel(CANVAS_WIDTH, CANVAS_HEIGHT, pixel)
        };
    }

    /// Resize the canvas to the correct size.
    ///
    /// # Params
    /// - `bigger: bool` are we resizing the canvas bigger or smaller.
    pub fn resize(&mut self) {
        // Resize it boy
        self.image = imageops::resize(&self.image, CANVAS_WIDTH, CANVAS_HEIGHT, imageops::FilterType::Nearest);
    }

    /// Shrink the canvas image, this helps out when working with CPU entusive Schemas.
    pub fn shrink(&mut self, factor: u32) {
        let width = CANVAS_WIDTH / factor;
        let height = CANVAS_HEIGHT / factor;

        self.image = imageops::resize(&self.image, width, height, imageops::FilterType::Nearest);
    }
}
