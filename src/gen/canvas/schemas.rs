use std::vec;

use crate::gen::types::SchemaSkipType;
use crate::learning::data_set::add_to_set;
use crate::learning::interface::predict_schema;
use crate::utils::image_utils::crop_image;
use crate::utils::randomify::randomify_color;
use crate::utils::{
    randomify::{random_skip_values, random_value},
    rgb_conversions::rgb_to_u8,
};

use super::base::Canvas;
use image::RgbImage;
use imageproc::{drawing, rect};
use rand::Rng;

impl Canvas {
    ///
    /// Draw a schema on the canvas.
    ///
    fn draw_schema(
        &mut self,
        schema_title: &str,
        f: fn(&mut RgbImage, (u32, u32), i32, Vec<(i32, i32, i32)>),
    ) {
        // Borrow the canvas image
        let image = self.image.clone();
        loop {
            // Grab dimensions of the canvas
            let (width, height) = self.image.dimensions();
            // Modulus, size, skips, skip_type
            let modulus = get_modulus();
            let size = get_draw_size(modulus);
            let skips = random_skip_values();
            let skip_type = SchemaSkipType::Original;
            // let color = self.cock_colors.random_color_from_pallete();
            let color = randomify_color();
            debug_schema(schema_title, &modulus, &size, &skips, &skip_type);
            
            // Check if we should verify the schema            
            if !self.train {
                let valid = predict_schema(schema_title.to_string(), modulus, size, skips.clone(), skip_type.to_string());
                println!("Valid schema: {}", valid);
                if !valid {
                    // Re run the loop
                    continue;
                }
            }
            
            for x in 0..width {
                for y in 0..height {
                    // Check for skip
                    if should_draw(
                        x as i32,
                        y as i32,
                        modulus.clone(),
                        size.clone(),
                        size.clone(),
                        Some(skips.clone()),
                        skip_type.clone(),
                    ) {
                        // println!("Draw!!!!");
                        f(&mut self.image, (x, y), modulus, vec![color]);
                    }
                }
            }
            // Check if we are adding to the Training Set
            if self.train {
                let valid = verify_schema(&self.image, color);
                add_to_set(schema_title.to_string(), modulus, size, skips, skip_type.to_string(), valid);
                if valid == 0 {
                    break;
                } else {
                    // Reset the image because its not valid
                    self.image = image.clone();
                }
            } else {
                break;
            }
        }
        // Crop the image
        self.image = crop_image(self.image.clone());
    }

    pub fn draw_circles(&mut self) {
        fn draw(
            image: &mut RgbImage,
            coordiantes: (u32, u32),
            size: i32,
            colors: Vec<(i32, i32, i32)>,
        ) {
            let color = random_value(&colors).clone();
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
        fn draw(
            image: &mut RgbImage,
            coordiantes: (u32, u32),
            size: i32,
            colors: Vec<(i32, i32, i32)>,
        ) {
            let color = random_value(&colors).clone();
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
        fn draw(
            image: &mut RgbImage,
            coordiantes: (u32, u32),
            size: i32,
            colors: Vec<(i32, i32, i32)>,
        ) {
            // Random color
            let color = randomify_color();
            // Random values because space is completely random
            let x = rand::thread_rng().gen_range(0..coordiantes.0 + 1);
            let y = rand::thread_rng().gen_range(0..coordiantes.1 + 1);
            drawing::draw_hollow_circle_mut(image, (x as i32, y as i32), size, rgb_to_u8(color));
        }
        self.draw_schema("Space", draw);
    }

    pub fn draw_stripes(&mut self) {
        fn draw(
            image: &mut RgbImage,
            coordiantes: (u32, u32),
            size: i32,
            colors: Vec<(i32, i32, i32)>,
        ) {
            let color = random_value(&colors).clone();
            // Start and end of line
            let start = (coordiantes.0 as f32, coordiantes.1 as f32);
            let end = (start.0 + size as f32, start.1 + size as f32);
            drawing::draw_line_segment_mut(image, start, end, rgb_to_u8(color));
        }
        self.draw_schema("Stripes", draw);
    }

    pub fn draw_curves(&mut self) {
        fn draw(
            image: &mut RgbImage,
            coordiantes: (u32, u32),
            size: i32,
            colors: Vec<(i32, i32, i32)>,
        ) {
            let color = random_value(&colors).clone();
            let (x, y) = (coordiantes.0 as i32, coordiantes.1 as i32);

            // Choose 4 random points
            let points = vec![(x, y), (x + size, y), (x, y + size), (x + size, y + size)];
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
}

///
/// The function that decides to skip a draw or not.
/// Decides based on the positions passed vs modulus.
///
/// # Params
/// - `pos1: i32` The first position to check.
/// - `pos2: i32` The second position to check.
/// - `modulus: i32` The modulus to check for.
/// - `remainder: i32` The remainder to check for.
/// - `values_against: Option<Vec<i32>>` The values to check against.
/// - `skip_type: SchemaSkipType` The type of skip to use.
///
/// # Returns
/// `bool` Whether to skip or not.
///
#[allow(unused_variables)]
fn should_draw(
    pos1: i32,
    pos2: i32,
    modulus: i32,
    remainder: i32,
    size: i32,
    values_against: Option<Vec<i32>>,
    skip_type: SchemaSkipType,
) -> bool {
    let values_against = {
        let def_values = vec![2, 3, 4, 5, 6, 7, 8];
        match values_against {
            Some(v) => {
                if v.is_empty() {
                    def_values
                } else {
                    v
                }
            }
            None => def_values,
        }
    };

    for value in values_against {
        if skip_type == SchemaSkipType::Original {
            if pos1 % value == remainder && pos2 % value == remainder {
                return true;
            }
        } else if skip_type == SchemaSkipType::V2 {
            // We want to skip the first value
            panic!("V2 not implemented");
        }
    }
    false // Default to false
}

///
/// Print to the screen the values of the draw.
///
/// # Params
/// - `draw_type: &str` The type of draw.
/// - `modulus: i32` The modulus value.
/// - `size: T` The size of the draw.
/// - `skip_values: Vec<i32>` The values to skip.
/// - `skip_type: &SchemaSkipType` The type of skip.
///
fn debug_schema(
    draw_type: &str,
    modulus: &i32,
    size: &i32,
    skip_values: &Vec<i32>,
    skip_type: &SchemaSkipType,
) {
    println!("{}", draw_type);
    println!("Modulus: {}", modulus);
    if size == &0 {
        println!("Size: random");
    } else {
        println!("Size: {}", size);
    }
    println!("Skip values: {:?}", skip_values);
    println!("Skip type: {:?}", skip_type);
    println!("===============================")
}

///
/// Get a random Modulus from certain possible values.
///
/// # Returns
/// `i32` The random modulus.
///
fn get_modulus() -> i32 {
    rand::thread_rng().gen_range(2..30)
}

///
/// Get a size for the draw object.
///
/// # Returns
/// `i32` The size of the draw.
///
fn get_draw_size(modulus: i32) -> i32 {
    rand::thread_rng().gen_range(1..modulus + 20)
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

    for (_, __, pixel) in image.enumerate_pixels() {
        if pixel == &rgb_to_u8((0, 0, 0)) || pixel == &rgb_to_u8((255, 255, 255)) {
            empty_count += 1;
        } else if pixel == &rgb_to_u8(color) {
            full_count += 1;
        }
    }

    if empty_count >= (image.width() * image.height() - 50) {
        valid = 1;
        println!("Empty");
    } else if full_count >= (image.width() * image.height() - 50) {
        valid = 2;
        println!("Full");
    }

    valid
}
