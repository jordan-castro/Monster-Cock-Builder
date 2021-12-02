use crate::gen::attributes::cocktributes::CockTribute;
use crate::gen::monster::monster_cock::MonsterCock;
use crate::gen::types::CockType;

impl MonsterCock {
    pub fn new(id: u32, cock_type: CockType, is_test_net: bool) -> MonsterCock {
        Self::base(
            id,
            generation_from_id(id),
            cock_type,
            String::new(),
            None,
            is_test_net,
        )
    }

    pub fn with_name(id: u32, cock_type: CockType, name: String, is_test_net: bool) -> MonsterCock {
        let mut monster = Self::base(
            id,
            generation_from_id(id),
            cock_type,
            String::new(),
            None,
            is_test_net,
        );
        monster.name = Self::format_name(name, id);
        monster
    }

    pub fn with_category(
        id: u32,
        cock_type: CockType,
        category: String,
        is_test_net: bool,
    ) -> MonsterCock {
        Self::base(
            id,
            generation_from_id(id),
            cock_type,
            category,
            None,
            is_test_net,
        )
    }

    pub fn with_name_and_category(
        id: u32,
        cock_type: CockType,
        name: String,
        category: String,
        is_test_net: bool,
    ) -> MonsterCock {
        let mut monster = Self::base(
            id,
            generation_from_id(id),
            cock_type,
            category,
            None,
            is_test_net,
        );
        monster.name = Self::format_name(name, id);
        monster
    }

    pub fn with_attributes(
        id: u32,
        cock_type: CockType,
        attributes: Vec<CockTribute>,
        is_test_net: bool,
        name: Option<String>,
        category: Option<String>,
    ) -> MonsterCock {
        let mut monster = Self::base(
            id,
            generation_from_id(id),
            cock_type,
            category.unwrap_or_default(),
            Some(attributes),
            is_test_net,
        );

        // Check if the name is set and is not equal to "random"
        if let Some(name) = name {
            if name != "random" {
                monster.name = Self::format_name(name, id);
            }
        }

        monster
    }

    fn format_name(name: String, id: u32) -> String {
        format!("{} #{}", name, id)
    }
}

/// Create the cock Generation based on a ID.
///
/// # Arguments
/// - `id: u32` The id of the cock.
///
/// # Returns
/// `u32` The generation of the cock.
fn generation_from_id(id: u32) -> u32 {
    // Geneartion is as follows
    // 0 - 50: 0
    // 51 - 100: 1
    // 101 - 150: 2
    // And so on...
    let generation = (id / 50) + 1;
    generation
}
