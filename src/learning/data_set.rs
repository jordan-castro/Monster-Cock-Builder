use std::{io::Write, thread};

use image::RgbImage;

use crate::{
    gen::canvas::{base::Canvas, schema::Schema},
    utils::rgb_conversions::rgb_to_u8,
};

/// Function that will create schemas in a loop for a given number of times.
/// The function will then put the data from the schema created in data/schemas.txt.
/// Uses Multithreading to speed up the process, so keep that in mind when you decide the number of schemas to create.
/// Any more than 50 schemas slows down a 16 gb Ram machine.
///
/// # Arguments
/// - `num_schemas` - The number of schemas to create
///
/// # Example
/// ```
/// use data::training_data;
///     
/// training_data(20);
/// ```
///
/// # Headers   
/// Type; Modulus; Size; Skip Values; Skip Type; Result
///
/// # Output
/// ```
/// Circles; 10; 5; [30,40,50]; original; 1
/// Squares; 15; 2; [2, 4, 6, 8]; v2; 0
/// ```
pub fn training_data(num_schemas: u32, save: bool) {
    let mut threads = Vec::new();
    for x in 0..num_schemas {
        let th = thread::spawn(move || {
            let mut canvas = Canvas::new(false, true);
            // Randomly draw the schemas
            let res = canvas.draw_space();
            if save {
                canvas
                    .image
                    .save(format!("data/canvases/canvas{}.png", x))
                    .unwrap();
            }
            // Verify and place accordingly
            verify_schema(res.0, &canvas.image, res.1);
        });
        threads.push(th);
    }
    for th in threads {
        th.join().unwrap();
    }
}

/// Add data to the schemas.txt file
///
/// # Arguments
/// - `schema: &Schema` The schema to add to the file.
/// - `result: i32` The result of the schema.
fn add_to_set(schema: &Schema, result: u32) {
    let mut file = std::fs::OpenOptions::new()
        .append(true)
        .open("data/schemas.txt")
        .expect("Unable to open file");

    let mut schema_string = String::new();
    schema_string.push_str(&schema.title);
    schema_string.push_str(";");
    schema_string.push_str(&schema.modulus.to_string());
    schema_string.push_str(";");
    schema_string.push_str(&schema.size.to_string());
    schema_string.push_str(";");
    schema_string.push_str(&schema.stringify_skips());
    schema_string.push_str(";");
    schema_string.push_str(&schema.skip_type.to_string());
    schema_string.push_str(";");
    schema_string.push_str(&result.to_string());
    schema_string.push_str("\n");
    file.write(schema_string.as_bytes())
        .expect("Unable to write to file");
}

///
/// Verify the schema
///
/// # Params
/// - `image: RgbImage` The image to verify.
/// - `color: (i32, i32, i32)` The color of the schema.
///    - By default if there is more than one color in the schema, then it is already verified.
fn verify_schema(schema: Schema, image: &RgbImage, color: (i32, i32, i32)) {
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
    let full_max = match schema.title.to_lowercase().as_str() {
        "circles" => image.width() * image.height() - 5000,
        "squares" => image.width() * image.height() - 5000,
        "stripes" => image.width() * image.height() - 5000,
        "space" => image.width() * image.height() - 7000,
        _ => 0,
    };
    let empty_max = match schema.title.as_str().to_lowercase().as_str() {
        "circles" => image.width() * image.height() / 2,
        "squares" => image.width() * image.height() / 2,
        "stripes" => image.width() * image.height() / 2, // The default
        "space" => full_max - 3000,
        _ => 0,
    };

    if empty_count > empty_max {
        add_to_set(&schema, 1);
        // valid = 1;
        println!("Empty");
    } else if full_count > full_max {
        // valid = 2;
        add_to_set(&schema, 2);
        println!("Full");
    } else {
        // valid = 0;
        add_to_set(&schema, 0);
        println!("Valid");
    }
}
