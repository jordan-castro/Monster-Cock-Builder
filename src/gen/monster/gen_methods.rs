use crate::gen::attributes::cocktributes::CockTribute;
use crate::gen::monster::monster_cock::MonsterCock;
use crate::gen::types::CockType;

impl MonsterCock {
    pub fn new(id: u32, generation: i32, cock_type: CockType, is_test_net: bool) -> MonsterCock {
        Self::base(id, generation, cock_type, String::new(), None, is_test_net)
    }

    pub fn with_name(id: u32, generation: i32, cock_type: CockType, name: String, is_test_net: bool) -> MonsterCock {
        let mut monster = Self::base(id, generation, cock_type, String::new(), None, is_test_net);
        monster.name = Self::format_name(name, id);
        monster
    }

    pub fn with_category(id: u32, generation: i32, cock_type: CockType, category: String, is_test_net: bool) -> MonsterCock {
        Self::base(id, generation, cock_type, category, None, is_test_net)
    }

    pub fn with_name_and_category(id: u32, generation: i32, cock_type: CockType, name: String, category: String, is_test_net: bool) -> MonsterCock {
        let mut monster = Self::base(id, generation, cock_type, category, None, is_test_net);
        monster.name = Self::format_name(name, id);
        monster
    }

    pub fn with_attributes(id: u32, generation: i32, cock_type: CockType, attributes: Vec<CockTribute>, is_test_net: bool) -> MonsterCock {
        Self::base(id, generation, cock_type, String::new(), Some(attributes), is_test_net)
    }

    fn format_name(name: String, id: u32) -> String {
        format!("{} #{}", name, id)
    }
}
