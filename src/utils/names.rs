use std::{fs, io::Write};

const NAMES_LOCATION: &str = "data/names.txt";

///
/// Open the file that contains the names and return the names.
/// 
/// # Params
/// - `is_test_net: bool` Is the name for a test net
/// 
/// # Returns
/// - `Vec<String>` The names.
/// 
pub (super) fn get_names(is_test_net: bool) -> Vec<String> {
    let black = black_listed(is_test_net);
    // Open the names file
    let names_file = fs::read_to_string(NAMES_LOCATION).unwrap();
    // Split the names into a vector
    let names: Vec<String> = names_file.split("\n").map(|s| s.to_string()).collect();
    // Go through each name and split the `\t` character
    let mut names_vec: Vec<String> = Vec::new();
    for name in names {
        let name_split: Vec<String> = name.split("\t").map(|s| s.to_string()).collect();
        if name_split.len() != 2 {
            continue;
        }
        // Check that name_split[1] contains a 'm' And that it is not blacklisted
        if name_split[1].contains("m") && !black.contains(&name_split[0]) {
            names_vec.push(name_split[0].to_string());
        }
    }
    // MALE NAMES
    names_vec
}

///
/// Add the name to the black list.
/// 
/// # Params
/// - `name: String` The name to blacklist.
/// - `is_test_net: bool` Is the name for a test net.
/// 
pub fn black_list_name(name: String, is_test_net: bool) {
    // Find the location
    let location = black_location(is_test_net);
    // Open the file
    let mut file = fs::OpenOptions::new()
        .append(true)
        .create(true)
        .open(location)
        .unwrap();
    // Write the name to the file
    file.write(format!("{}\n", name).as_bytes()).unwrap();
}

///
/// Grab the black listed names
/// 
/// # Params
/// - `is_test_net: bool` Is the name for a test net.
/// 
/// # Returns
/// - `Vec<String>` The black listed names.
/// 
fn black_listed(is_test_net: bool) -> Vec<String> {
    let location = black_location(is_test_net);
    let file = fs::read_to_string(location).unwrap();
    let names: Vec<String> = file.split("\n").map(|s| s.to_string()).collect();
    names
}

fn black_location(is_test_net: bool) -> String {
    format!("data/{}/blacklistnames.txt", if is_test_net { "testnet" } else { "mainnet" })
}