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