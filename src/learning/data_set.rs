use std::{io::Write, thread};

use image::{RgbImage, Rgb, imageops};
use rand::Rng;

use crate::{
    gen::canvas::{base::Canvas, schema::Schema}, utils::randomify::random_value,
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
    // Lambda function that takes in a (Schema, (i32,i32,i32)) and a u32 and a string
    let drawer = |res: (Schema, (i32, i32, i32)), i: u32, filename: &str, canvas: &mut Canvas, save: bool| {
        if save {
            canvas.image.save(format!("data/canvases/{}{}.png", filename, i)).unwrap();
        }
        verify_schema(res.0, &mut canvas.image);
        canvas.clear();
    };

    let mut current_number = 0;
    // Find the number of canvases we are on.
    // Get the files in the data/canvases folder
    let files = glob::glob("data/canvases/*.png").unwrap();
    // Loop through the files and find the number of canvases
    for f in files {
        let file = f.unwrap();
        let filename = file.file_name().unwrap().to_str().unwrap();
        // Strip from .png
        let filename = filename.split(".").collect::<Vec<&str>>()[0];
        // Get the number which is the last char
        let number = filename.chars().last().unwrap().to_string().parse::<u32>().unwrap();
        if number > current_number {
            current_number = number;
        }
    }
    current_number += 1;

    for x in 0..num_schemas {
        let th = thread::spawn(move || {
            // Random ligth base
            let is_light: bool = *random_value(&vec![true, false]);

            let mut canvas = Canvas::new(is_light, true);

            let i = x + current_number;
            let result = canvas.draw_circles();
            drawer(result, i, "circles", &mut canvas, save);

            let result = canvas.draw_squares();
            drawer(result, i, "squares", &mut canvas, save);

            let result = canvas.draw_stripes();
            drawer(result, i, "stripes", &mut canvas, save);

            let result = canvas.draw_space();
            drawer(result, i, "space", &mut canvas, save);

            let result = canvas.draw_squares_with_gradients();
            canvas.resize();
            drawer(result, i, "gsquares", &mut canvas, save);
        });
        threads.push(th);
    }
    for th in threads {
        th.join().expect("Joining thread");
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
fn verify_schema(schema: Schema, image: &mut RgbImage) {
    // Crop the image
    let image = imageops::crop(image, 100, 100, image.width() - 100, image.height() - 100);
    let sub_image = image.to_image();

    sub_image.save(format!("{}_canvas.png", schema.title)).unwrap();

    // Get the width and height of the image
    let image_width = sub_image.width();
    let image_height = sub_image.height();

    let mut rows: Vec<Vec<Rgb<u8>>> = Vec::new();
    let mut amount: u32 = 0; // Todo change name

    // Loop through the rows of pixels in the image
    for y in 0..image_height {
        let mut row: Vec<Rgb<u8>> = Vec::new();
        // Loop through the pixels in the row
        for x in 0..image_width {
            // Get the pixel at the x,y position
            let pixel = sub_image.get_pixel(x, y);
            // Push the pixel
            row.push(*pixel);
        }
        // Add the row to the rows vector
        rows.push(row);
    }

    // Now loop through the rows and remove any repeated pixels
    for row in rows.iter_mut() {
        row.dedup();
        // Check the lenght of row
        if row.len() > 1 {
            amount += 1;
        }
    }

    if amount > 100 {
        println!("Valid schema for {}", schema.title);
        add_to_set(&schema, 1);
    } else {
        println!("Invalid schema for {}", schema.title);
        add_to_set(&schema, 0);
    }
}