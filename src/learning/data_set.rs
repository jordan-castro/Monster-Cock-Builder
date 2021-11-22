use std::{io::Write, thread};

use crate::{
    gen::{canvas::base::Canvas, colors::CockColors, types::CockType},
    utils::randomify::randomattributes,
};
use itertools::Itertools;

///
/// Function that will create schemas in a loop for a given number of times.
/// The function will then put the data from the schema created in data/schemas.txt.
/// Used Multithreading to speed up the process, so keep that in mind when you decide the number of schemas to create.
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
/// Circles; 10; 5; [30,40,50]; Original; 1
/// Squares; 15; 2; [2, 4, 6, 8]; Original; 0
/// ```
///  
pub fn training_data(num_schemas: u32) {
    let mut threads = Vec::new();
    for _ in 0..num_schemas {
        let th = thread::spawn(|| {
            let mut canvas = Canvas::new(
                randomattributes(0),
                CockColors::new(CockType::Default, String::new()),
                true,
                true
            );
            canvas.draw_stripes();
        });
        threads.push(th);
    }
    for th in threads {
        th.join().unwrap();
    }
}

///
/// Add data to the schemas.txt file
///
/// # Arguments
/// `schema_type: String` The type of schema to add
/// `modulus: i32` The modulus of the schema
/// `size: i32` The size of the schema
/// `skips: Vec<i32>` The skip values of the schema
/// `skip_type: String` The skip type of the schema
/// `result: i32` The result of the schema
///
pub fn add_to_set(
    schema_type: String,
    modulus: i32,
    size: i32,
    skips: Vec<i32>,
    skip_type: String,
    result: u32,
) {
    let mut file = std::fs::OpenOptions::new()
        .append(true)
        .open("data/schemas.txt")
        .expect("Unable to open file");

    let skips = if skips.is_empty() {
        vec![2, 3, 4, 5, 6, 7, 8]
    } else {
        skips
    };

    let mut schema_string = String::new();
    schema_string.push_str(&schema_type);
    schema_string.push_str(";");
    schema_string.push_str(&modulus.to_string());
    schema_string.push_str(";");
    schema_string.push_str(&size.to_string());
    schema_string.push_str(";");
    schema_string.push_str(&skips.iter().join(","));
    schema_string.push_str(";");
    schema_string.push_str(&skip_type);
    schema_string.push_str(";");
    schema_string.push_str(&result.to_string());
    schema_string.push_str("\n");
    file.write(schema_string.as_bytes())
        .expect("Unable to write to file");
}
