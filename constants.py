K_ATTRIBUTES = [
    'Strength',
    'Speed',
    'Intellect',
    'Combat',
    'Sanity',
    'Fear',
    'Body'
]

K_TRAINED_SKILLS = [
    'Linguistics',
    'Zoology',
    'Botany',
    'Geology',
    'Industrial Equipment',
    'Jury-Rigging',
    'Chemistry',
    'Computers',
    'Zero-G',
    'Mathematics',
    'Art',
    'Archaeologist',
    'Theology',
    'Military Training',
    'Rimwise',
    'Athletics'
]

K_EXPERT_SKILLS = [
    'Psychology',
    'Pathology',
    'Field Medicine',
    'Ecology',
    'Asteroid Mining',
    'Mechanical Repair',
    'Explosives',
    'Pharmacology',
    'Hacking',
    'Piloting',
    'Physics',
    'Mysticism',
    'Wilderness Survival',
    'Firearms',
    'Hand-to-hand Combat'
]

K_MASTER_SKILLS = [
    'Sophontology',
    'Exobiology',
    'Surgery',
    'Planetology',
    'Robotics',
    'Engineering',
    'Cybernetics',
    'Artificial Intelligences',
    'Hyperspace',
    'Xenoesotericsm',
    'Command'
]

K_SKILLS = K_TRAINED_SKILLS + K_EXPERT_SKILLS + K_MASTER_SKILLS

# Mothership 1e Panic Check table: 1d20 roll -> (name, effect)
K_PANIC_EFFECT = {
    1: (
        'Adrenaline Rush',
        '[+] on all rolls for the next 2d10 minutes. Reduce Stress by 1d5.',
    ),
    2: (
        'Nervous',
        'Gain 1 Stress.',
    ),
    3: (
        'Jumpy',
        'Gain 1 Stress. All Close crewmembers gain 2 Stress.',
    ),
    4: (
        'Overwhelmed',
        '[-] on all rolls for the next 1d10 minutes. Increase Minimum Stress by 1.',
    ),
    5: (
        'Coward',
        'Gain a new Condition: You must make a Fear Save to engage in violence, otherwise you flee.',
    ),
    6: (
        'Frightened',
        'Gain a new Condition: When encountering what frightened you, make a Fear Save [-] or gain 1d5 Stress.',
    ),
    7: (
        'Nightmares',
        'Gain a new Condition: Sleep is difficult, gain [-] on Rest Saves.',
    ),
    8: (
        'Loss of Confidence',
        "Gain a new Condition: Choose one Skill and lose that Skill's bonus.",
    ),
    9: (
        'Deflated',
        'Gain a new Condition: Whenever a Close crewmember fails a Save, gain 1 Stress.',
    ),
    10: (
        'Doomed',
        'Gain a new Condition: You feel cursed and unlucky. All Critical Successes are instead Critical Failures.',
    ),
    11: (
        'Suspicious',
        'For the next week, whenever someone joins the crew (even if they only left for a short period of time), make a Fear Save or gain 1 Stress.',
    ),
    12: (
        'Haunted',
        'Gain a new Condition: Something starts visiting the character at night. In their dreams. Out of the corner of their eye. And soon it will start making demands.',
    ),
    13: (
        'Death Wish',
        'For the next 24 hours, whenever encountering a stranger or known enemy, make a Sanity Save or immediately attack them.',
    ),
    14: (
        'Prophetic Vision',
        'Character immediately experiences an intense hallucination or vision of an impending terror or horrific event. Increase Minimum Stress by 2.',
    ),
    15: (
        'Catatonic',
        'Become unresponsive and unmoving for 2d10 minutes. Reduce Stress by 1d10.',
    ),
    16: (
        'Rage',
        '[+] on all Damage rolls for the next 1d10 hours. All crewmembers gain 1 Stress.',
    ),
    17: (
        'Spiraling',
        'Gain a new Condition: Panic Checks are at [-].',
    ),
    18: (
        'Compounding Problems',
        'Roll twice on this table. Increase your Minimum Stress by 1.',
    ),
    19: (
        'Heart Attack / Short Circuit (Androids)',
        'Reduce Maximum Wounds by 1. Gain [-] on all rolls for 1d10 hours. Increase Minimum Stress by 1.',
    ),
    20: (
        'Retire',
        'Roll up a new character to play.',
    ),
}

# Reverse lookup: panic effect name -> 1d20 roll
K_PANIC_EFFECT_INDEX = {name: roll for roll, (name, _) in K_PANIC_EFFECT.items()}
# Mothership 1e Wounds table: 1d10 roll (0-9) -> severity
K_WOUND_SEVERITY = {
    0: 'Flesh Wound',
    1: 'Minor Injury',
    2: 'Minor Injury',
    3: 'Minor Injury',
    4: 'Minor Injury',
    5: 'Major Injury',
    6: 'Major Injury',
    7: 'Lethal Injury (Death Save in 1d10 rounds)',
    8: 'Lethal Injury (Death Save in 1d10 rounds)',
    9: 'Fatal Injury (Death Save)',
}

# Mothership 1e Wounds table, per wound type: 1d10 roll (0-9) -> effect
K_WOUND_BLUNT_FORCE = {
    0: 'Knocked down.',
    1: "Winded. [-] until you catch your breath.",
    2: 'Sprained Ankle. [-] on Speed Checks.',
    3: 'Concussion. [-] on mental tasks.',
    4: 'Leg or foot broken. [-] on Speed Checks.',
    5: 'Arm or hand broken. [-] manual tasks.',
    6: 'Snapped collarbone. [-] on Strength Checks.',
    7: 'Back broken. [-] on all rolls.',
    8: 'Skull fracture. [-] on all rolls.',
    9: 'Spine or neck broken. Death Save.',
}

K_WOUND_BLEEDING = {
    0: 'Drop held item.',
    1: 'Lots of blood. Those Close gain 1 Stress.',
    2: 'Blood in eyes. [-] until wiped clean.',
    3: 'Laceration. Bleeding +1.',
    4: 'Major cut. Bleeding +2.',
    5: 'Fingers/toes severed. Bleeding +3.',
    6: 'Hand/foot severed. Bleeding +4.',
    7: 'Limb severed. Bleeding +5.',
    8: 'Major artery cut. Bleeding +6.',
    9: 'Throat slit or heart pierced. Death Save.',
}

K_WOUND_GUNSHOT = {
    0: 'Grazed. Knocked down.',
    1: 'Bleeding +1.',
    2: 'Broken rib.',
    3: 'Fractured extremity.',
    4: 'Internal bleeding. Bleeding +2.',
    5: 'Lodged bullet. Surgery required.',
    6: 'Gunshot wound to the neck.',
    7: 'Major blood loss. Bleeding +4.',
    8: 'Sucking chest wound. Bleeding +5.',
    9: 'Headshot. Death Save.',
}

K_WOUND_FIRE_EXPLOSIVES = {
    0: 'Hair burnt. Gain 1d5 Stress.',
    1: 'Awesome scar. +1 Minimum Stress.',
    2: 'Singed. [-] on next action.',
    3: 'Shrapnel/large burn.',
    4: 'Extensive burns. -1d10 Strength.',
    5: 'Major Burn. -2d10 Body Save.',
    6: 'Skin grafts required. -2d10 Body Save.',
    7: 'Limb on fire. 2d10 Damage per round.',
    8: 'Body on fire. 3d10 Damage per round.',
    9: 'Engulfed in fiery explosion. Death Save.',
}

K_WOUND_GORE_MASSIVE = {
    0: 'Vomit. [-] on next action.',
    1: 'Awesome scar. +1 Minimum Stress.',
    2: 'Digit mangled.',
    3: 'Eyes gouged out.',
    4: 'Ripped off flesh. -1d10 Strength.',
    5: 'Paralyzed waist down.',
    6: 'Limb severed. Bleeding +5.',
    7: 'Impaled. Bleeding +6.',
    8: 'Guts spooled on floor. Bleeding +7.',
    9: 'Head explodes. No Death Save. You have died.',
}

# Wound type name -> its effect table
K_WOUNDS = {
    'Blunt Force': K_WOUND_BLUNT_FORCE,
    'Bleeding': K_WOUND_BLEEDING,
    'Gunshot': K_WOUND_GUNSHOT,
    'Fire & Explosives': K_WOUND_FIRE_EXPLOSIVES,
    'Gore & Massive': K_WOUND_GORE_MASSIVE,
}

K_WOUND_TYPES = list(K_WOUNDS)

# Embed color for neutral messages, by the quarter of the character
K_NEUTRAL_COLOR = 0x3498DB
K_QUARTER_COLORS = {
    'North': 0xC7A547,
    'South': 0xCF5539,
    'East': 0x45CC63,
    'West': 0x44BBD8,
}

