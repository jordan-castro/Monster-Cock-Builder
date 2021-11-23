use std::{io::Write, thread};

use crate::{gen::{canvas::{base::Canvas, schema::Schema}, colors::CockColors, types::CockType}, utils::randomify::randomattributes};

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
            // Randomly draw the schemas
            canvas.draw_circles();
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
/// - `schema: &Schema` The schema to add to the file.
/// - `result: i32` The result of the schema.
///
pub fn add_to_set(
    schema: &Schema,
    result: u32,
) {
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
