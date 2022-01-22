use std::process::Command;
use serde_json::Value;

use crate::gen::{canvas::schema::Schema, types::SchemaSkipType};

/// Call the pythonn ML model that will write a schema for us.
pub fn make_schema(title: String) -> Schema {
    println!("Making schema for {}", title);
    // Open a new process to verify the schema
    let mut result = Command::new("scripts/verify.bat");
    // Add the title to the command
    result.arg(title);
    // Run the process
    result.spawn().expect("Unable to spawn process");
    let path_to_json = "schema.json";

    // Open and read the JSON file
    let schema_json = std::fs::read_to_string(path_to_json).unwrap();
    // Read the JSON
    let schema_json: Value = serde_json::from_str(&schema_json).unwrap();
    
    // Skips has some special work done to it before it goes into the Struct
    let skips = {
        let skips_json = schema_json["skips"].as_array().unwrap();
        skips_json.iter().map(|x| x.as_i64().unwrap() as i32).collect()
    };

    Schema {
        title: schema_json["Type"].as_str().unwrap().to_string(),
        modulus: schema_json["Modulus"].as_i64().unwrap() as i32,
        size: schema_json["Size"].as_i64().unwrap() as i32,
        skips,
        skip_type: SchemaSkipType::from_string(schema_json["Skip Type"].as_str().unwrap().to_string()),
    }
}