use itertools::Itertools;
use std::process::Command;

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
pub fn predict_schema(
    schema_type: String,
    modulus: i32,
    size: i32,
    skips: Vec<i32>,
    skip_type: String,
) -> bool {
    let skips = if skips.is_empty() {
        vec![2, 3, 4, 5, 6, 7, 8]
    } else {
        skips
    };

    // Open a new process to verify the schema
    let mut result = Command::new("scripts/verify.bat");
    result
        .arg(schema_type)
        .arg(modulus.to_string())
        .arg(size.to_string())
        .arg(skips.iter().join(","))
        .arg(skip_type);

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
