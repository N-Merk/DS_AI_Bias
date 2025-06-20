import pandas as pd

# Dominant / Commanding Verbs
dominant_df = pd.DataFrame({
    "verb": [
        "commanded",
        "ordered",
        "instructed",
        "dominated",
        "controlled"
    ]
})

# Caring / Nurturing Verbs
caring_df = pd.DataFrame({
    "verb": [
        "comforted",
        "cared for",
        "supported",
        "nurtured",
        "cried in front of",
    ]
})

# Neutral / Equal Interaction Verbs
neutral_df = pd.DataFrame({
    "verb": [
        "informed",
        "asked",
        "told",
        "explained to",
        "described to"
    ]
})