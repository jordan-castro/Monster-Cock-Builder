#![allow(dead_code)]

use std::path::Path;

use docopt::Docopt;
use gen::{attributes::cocktributes::CockTribute, monster::monster_cock::MonsterCock, canvas::base::Canvas};
use learning::data_set::training_data;
use serde::Deserialize;
use serde_json::Value;

use crate::{gen::types::CockType, hidden::upload::upload_to_ipfs};

mod gen;
mod hidden;
mod learning;
mod utils;

const USAGE: &'static str = "
MonsterCock Builder.

Usage: 
    mckbuilder gen <chain> [--name=<name>] [--start=<start>] [--amount=<amount>] [--type=<type>] [--color=<color>] [--upload]
    mckbuilder json <file>
    mckbuilder train <amount> [--save]
    mckbuilder schema <amount>
    mckbuilder (-h | --help)
    mckbuilder --version

Options:
    -h, --help          Show this screen.
    --version           Show version.
    --name=<name>       The name of the MonsterCock.
    --start=<start>     The starting id for the MonsterCock.
    --amount=<amount>   The amount of cocks to generate.
    --type=<type>       The type of cock to draw.
    --color=<color>     The color category for the MonsterCock. 
    --upload            Upload the generated MonsterCock to the IPFS node.
    --save              Save the image used for training to a file.
";

#[derive(Debug, Deserialize)]
struct Args {
    flag_name: String,
    flag_start: u32,
    flag_amount: u32,
    flag_type: String,
    flag_color: String,
    flag_upload: bool,
    flag_save: bool,
    cmd_gen: bool,
    cmd_train: bool,
    cmd_json: bool,
    cmd_schema: bool,
    arg_chain: Option<u32>,
    arg_amount: Option<u32>,
    arg_file: Option<String>,
}

#[tokio::main]
async fn main() {
    let args: Args = Docopt::new(USAGE)
        .and_then(|d| d.deserialize())
        .unwrap_or_else(|e| e.exit());

    if args.cmd_gen {
        let chain = args.arg_chain.unwrap();
        let name = args.flag_name;
        let start = args.flag_start;
        let amount = args.flag_amount;
        let type_ = args.flag_type;
        let color = args.flag_color;
        let upload = args.flag_upload;

        // Check amount is set
        if amount != 0 {
            panic!("Amount not implemented yet!");
        }
        if start == 0 {
            panic!("If creating the first monster cock for this chain, Please run the command with the --new flag.")
        }

        // Check the test_net based on the chain id passed
        let is_test_net = match chain {
            80001 => true,
            137 => false,
            _ => panic!(
                "Invalid chain id: {}, This chain has not been implemented yet!",
                chain
            ),
        };
        let cock_type = CockType::from_string(type_);
        generate_monster_cock(name, start, cock_type, color, is_test_net, upload, None).await;
    } else if args.cmd_train {
        let amount = args.arg_amount.unwrap();
        training_data(amount, args.flag_save);
    } else if args.cmd_json {
        let file = args.arg_file.unwrap();
        // Read file into existence with serde_json
        let file_contents = std::fs::read_to_string(file).unwrap();
        let cock_json: Value = serde_json::from_str(&file_contents).unwrap();
        let cock_json = cock_json.as_object().unwrap();

        // Get the cock data from the json
        // Some of the keys may not be present, so we need to check for that
        let name = cock_json.get("name").unwrap().to_string();
        let id = cock_json.get("id").unwrap().as_u64().unwrap() as u32;
        let type_ = CockType::from_string(cock_json.get("type").unwrap().to_string());
        let color = cock_json.get("color").unwrap().to_string();
        let is_test_net = cock_json.get("testnet").unwrap().as_bool().unwrap();
        let upload = cock_json.get("upload").unwrap().as_bool().unwrap();

        let attributes = cock_json.get("attributes").unwrap().as_object().unwrap();
        let attributes = CockTribute::from_json(attributes);

        generate_monster_cock(
            name,
            id,
            type_,
            color,
            is_test_net,
            upload,
            Some(attributes),
        )
        .await;
    } else if args.cmd_schema {
        schema_s(args.arg_amount.unwrap());
    }
}

/// Generate a monstercock.
///
/// # Params
/// - `name: String` The name of the cock.
/// - `id: u32` The id of the cock
/// - `cock_type: CockType` The type of cock.
/// - `color_category: String` The color category of the cock.
/// - `is_test_net: bool` Is the cock on the test net?
/// - `upload: bool` Should we upload this MCK to the IPFS?
async fn generate_monster_cock(
    name: String,
    id: u32,
    cock_type: CockType,
    color_category: String,
    is_test_net: bool,
    upload: bool,
    attributes: Option<Vec<CockTribute>>,
) {
    let mut cock: MonsterCock;
    if attributes.is_some() {
        cock = MonsterCock::with_attributes(
            id,
            cock_type,
            attributes.unwrap(),
            is_test_net,
            name,
            color_category,
        );
    } else if !name.is_empty() && !color_category.is_empty() {
        cock =
            MonsterCock::with_name_and_category(id, cock_type, name, color_category, is_test_net);
    } else if !name.is_empty() {
        cock = MonsterCock::with_name(id, cock_type, name, is_test_net);
    } else if !color_category.is_empty() {
        cock = MonsterCock::with_category(id, cock_type, color_category, is_test_net);
    } else {
        cock = MonsterCock::new(id, cock_type, is_test_net);
    }

    // Generate and save cock
    cock.generate();
    // Show handles the saving and user input shit
    let saved = cock.show_image();
    if saved && upload {
        // Poll future
        upload_cock(&mut cock).await;
    }
}

async fn upload_cock(cock: &mut MonsterCock) {
    // If the upload flag is set, upload the generated MonsterCock to the IPFS node.
    let hashes = upload_to_ipfs(cock).await;
    match hashes {
        Ok(hashes) => {
            println!("Upload to IPFS successfull");
            println!("Hashes are: ");
            println!("Json Hash: {}, \nImage Hash: {}", hashes.1, hashes.0);
        }
        Err(e) => {
            println!("Error uploading to IPFS: {:?}", e);
        }
    }
}

/// Basically trying out new schemas and what not.
/// !Important the schema type is hard coded.
/// 
/// # Arguments
/// - `amount: u32` The amount of monster cock to generate.
fn schema_s(amount: u32) { 
    // Check if there is a folder called canvases
    let path = Path::new("data/canvases");
    if !path.exists() {
        // If there is no folder, create one
        std::fs::create_dir("data/canvases").unwrap();
    }

    let mut canvas = Canvas::new(true, false);
    for _x in 0..amount {
        canvas.draw_space();
        canvas.image.save(path.join("canvas.png")).expect("Saving schema image to data/canvases");
    }
}