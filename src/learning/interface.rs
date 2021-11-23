use std::process::Command;
use std::thread::{self, JoinHandle};

use crate::gen::canvas::schema::{self, Schema};
use crate::gen::types::SchemaSkipType;
use crate::utils::randomify::random_value;

// Use the correct python interpreter
const PYTHON_INTERPRETER: &str = r"C:\Users\jorda\miniconda3\envs\schema_verifier\python.exe";

// TODO: Multiple predictions with threading?

/// Verify a schema.
///
/// # Params
/// - `schema_type`: The schema to verify.
/// - `modulus: i32` The modulus.
/// - `size: i32` The size of the schema.
/// - `skips: Vec<i32>` The skip values.
/// - `skip_type: String` The skip type.
///
/// # Returns
/// - `bool` True if the schema is valid, false otherwise.  
fn predict_schema(schema_values: &Schema) -> bool {
    // Open a new process to verify the schema
    let mut result = Command::new("scripts/verify.bat");
    result
        .arg(schema_values.title.to_string())
        .arg(schema_values.modulus.to_string())
        .arg(schema_values.size.to_string())
        .arg(schema_values.stringify_skips())
        .arg(schema_values.skip_type.to_string());

    // Read the output of the process
    let data = result.output().expect("Unable to run process");
    // Convert the output to a string, split it, and collect the 3rd element which holds the prediction
    let output = String::from_utf8_lossy(&data.stdout);
    let output = output.trim();
    let output = output.split('\n').collect::<Vec<&str>>();
    let result = output[3].trim();

    if result == "1" {
        true
    } else {
        false
    }
}

/// Get valid schema values based on the schema type.
///
/// # Params
/// - `schema_type`: The schema type.
///
/// # Returns
/// - `value: SchemaValues` The valid schema values.
pub fn valid_schema(schema_type: &str) -> Schema {
    // // Threads
    // let mut threads: Vec<JoinHandle<Option<Schema>>> = Vec::new();
    // The valid schemas
    // let mut valids: Vec<Schema> = Vec::new();
    let mut schema: Schema;

    loop {
        schema = Schema::random_schema(schema_type.to_string());
        let res = predict_schema(&schema);
        println!("{}", res);
        if res {
            break;
        }
    }
    println!("Found schema!");
    schema

    // // We do 10 threads at a time
    // for _ in 0..10 {
    //     let t = loop {
    //         // Create a random schema
    //         let schema = Schema::random_schema(schema_type.to_string());
    //         // Thread it
    //         let t = thread::spawn(move || {
    //             // Predict the schema
    //             let result = predict_schema(&schema);
    //             if result {
    //                 Some(schema)
    //             } else {
    //                 None
    //             }
    //         });
    //         t
    //     };
    // }

    // // Loop through threads and grab results
    // for t in threads {
    //     let res = t.join().unwrap();
    //     if let Some(schema) = res {
    //         valids.push(schema);
    //     }
    // }

    // Choose a random valud of the valid schemas
    // random_value(&valids).clone()
}
