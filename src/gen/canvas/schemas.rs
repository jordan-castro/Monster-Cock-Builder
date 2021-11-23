use std::vec;

use crate::gen::types::SchemaSkipType;
use crate::learning::data_set::add_to_set;
use crate::learning::interface::valid_schema;
use crate::utils::image_utils::crop_image;
use crate::utils::randomify::randomify_color;
use crate::utils::rgb_conversions::rgb_to_u8;

use super::base::Canvas;
use super::schema::Schema;
use image::RgbImage;
use imageproc::{drawing, rect};
use rand::Rng;

impl Canvas {
    /// Draw a schema on the canvas.
    fn draw_schema(
        &mut self,
        schema_title: &str,
        f: fn(&mut RgbImage, (u32, u32), i32, (i32, i32, i32)),
    ) {
        // Grab dimensions of the canvas
        let (width, height) = self.image.dimensions();
        // let schema = Schema::random_schema(schema_title.to_string());
        let schema = if !self.train {
            valid_schema(schema_title)
        } else {
            Schema::random_schema(schema_title.to_string())
        };
        schema.debug();

        let color = randomify_color();

        for x in 0..width {
            for y in 0..height {
                // Check for skip
                if should_draw(x as i32, y as i32, &schema) {
                    // println!("Draw!!!!");
                    f(&mut self.image, (x, y), schema.size, color);
                }
            }
        }
        self.training_data(&schema, color);

        // Crop the image
        self.image = crop_image(self.image.clone());
    }

    /// Decides to keep creating the schema or not.
    /// And add to the Training set if self.train is true.
    fn training_data(&self, schema: &Schema, color: (i32, i32, i32)) {
        // Check if training
        if self.train {
            // Verify the schema
            let valid = verify_schema(&self.image, color);
            println!("Valid: {}", valid);
            // Add to the training set
            add_to_set(schema, valid);
        }
    }

    pub fn draw_circles(&mut self) {
        fn draw(image: &mut RgbImage, coordiantes: (u32, u32), size: i32, color: (i32, i32, i32)) {
            drawing::draw_hollow_circle_mut(
                image,
                (coordiantes.0 as i32, coordiantes.1 as i32),
                size,
                rgb_to_u8(color),
            );
        }
        self.draw_schema("Circles", draw);
    }

    pub fn draw_squares(&mut self) {
        fn draw(image: &mut RgbImage, coordiantes: (u32, u32), size: i32, color: (i32, i32, i32)) {
            /* Squares need a Rect. Made as follows:
            (x, y) is the top left corner of the rectangle
                X comes from coordinates.0
                Y comes from coordinates.1
            (width, height) is the width and height of the rectangle
                Width comes from size
                Height comes from size
            */
            drawing::draw_hollow_rect_mut(
                image,
                rect::Rect::at(coordiantes.0 as i32, coordiantes.1 as i32)
                    .of_size(size as u32, size as u32),
                rgb_to_u8(color),
            );
        }
        self.draw_schema("Squares", draw);
    }

    pub fn draw_space(&mut self) {
        #[allow(unused_variables)]
        fn draw(image: &mut RgbImage, coordiantes: (u32, u32), size: i32, color: (i32, i32, i32)) {
            // Random values because space is completely random
            let x = rand::thread_rng().gen_range(0..coordiantes.0 + 1);
            let y = rand::thread_rng().gen_range(0..coordiantes.1 + 1);
            drawing::draw_hollow_circle_mut(image, (x as i32, y as i32), size, rgb_to_u8(color));
        }
        self.draw_schema("Space", draw);
    }

    pub fn draw_stripes(&mut self) {
        fn draw(image: &mut RgbImage, coordiantes: (u32, u32), size: i32, color: (i32, i32, i32)) {
            // Start and end of line
            let start = (coordiantes.0 as f32, coordiantes.1 as f32);
            let end = (start.0 + size as f32, start.1 + size as f32);
            drawing::draw_line_segment_mut(image, start, end, rgb_to_u8(color));
        }
        self.draw_schema("Stripes", draw);
    }

    pub fn draw_curves(&mut self) {
        fn draw(image: &mut RgbImage, coordiantes: (u32, u32), size: i32, color: (i32, i32, i32)) {
            let (x, y) = (coordiantes.0 as i32, coordiantes.1 as i32);
            // Choose 4 points based on the size
            let points = vec![
                (x, y), 
                (x + (size * 2), y), 
                (x, y + (size * 2)), 
                (x + size, y + size)
                ];
            // Convert to f32
            let points = points
                .iter()
                .map(|(x, y)| (*x as f32, *y as f32))
                .collect::<Vec<(f32, f32)>>();

            drawing::draw_cubic_bezier_curve_mut(
                image,
                points[0],
                points[1],
                points[2],
                points[3],
                rgb_to_u8(color.clone()),
            );
        }
        self.draw_schema("Curves", draw);
    }

    /// Draw crosses
    pub fn draw_crosses(&mut self) {
        fn draw(image: &mut RgbImage, coordiantes: (u32, u32), size: i32, color: (i32, i32, i32)) {
            let (x, y) = (coordiantes.0 as i32, coordiantes.1 as i32);
            drawing::draw_cross_mut(image, rgb_to_u8(color), x, y)
        }
        self.draw_schema("Crosses", draw);
    }
}

///
/// The function that decides to skip a draw or not.
/// Decides based on the positions passed vs modulus.
///
/// # Params
/// - `pos1: i32` The first position to check.
/// - `pos2: i32` The second position to check.
/// - `schema: Schema` The schena being drawn.
///
/// # Returns
/// `bool` Whether to skip or not.
///
fn should_draw(pos1: i32, pos2: i32, schema: &Schema) -> bool {
    if schema.skip_type == SchemaSkipType::Original {
        if pos1 % schema.modulus == 0 || pos2 % schema.modulus == 0 {
            if (pos1 % 20 != 0 || pos1 % 15 != 0) || (pos2 % 15 != 0 || pos2 % 20 != 0) {
                return false;
            }
        } else {
            if (pos1 % 20 != 0 && pos1 % 15 != 0) || (pos2 % 15 != 0 && pos2 % 20 != 0) {
                return false;
            }
        }
    } else if schema.skip_type == SchemaSkipType::V2 {
        for value in schema.skips.iter() {
            if !(pos1 % value == 0 && pos2 % value == 0) {
                return false;
            }
        }
    }
    true // Default to true
}

///
/// Verify the schema
///
/// # Params
/// - `image: RgbImage` The image to verify.
/// - `color: (i32, i32, i32)` The color of the schema.
///    - By default if there is more than one color in the schema, then it is already verified.
///
/// # Returns
/// `u32 number` Whether the schema is valid or not.
///
fn verify_schema(image: &RgbImage, color: (i32, i32, i32)) -> u32 {
    let mut valid = 0;
    let mut empty_count = 0;
    let mut full_count = 0;

    // Loop through the image and check the pixel
    for (_, __, pixel) in image.enumerate_pixels() {
        if pixel == &rgb_to_u8((0, 0, 0)) || pixel == &rgb_to_u8((255, 255, 255)) {
            empty_count += 1;
        } else if pixel == &rgb_to_u8(color) {
            full_count += 1;
        }
    }
    let empty_max = image.width() * image.height() / 2;
    let full_max = image.width() * image.height() - 5000;

    if empty_count > empty_max {
        valid = 1;
        println!("Empty");
    } else if full_count > full_max {
        valid = 2;
        println!("Full");
    }

    valid
}
