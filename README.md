# CS555-Agille-Methods

## Testing
Run the following command under project folder to perform unit tests

```bash
python3 -m unittest discover -s tests -p Test*.py -v
```

## Format

### Individuals:

```json
{
    "@I1@": {
        "ID": "@I1@",
        "NAME": "Emme /Taylor/",
        "SEX": "F",
        "BIRT": "20 MAR 1949",
        "DEAT": "N/A",
        "WIFE": [
            "@F1@"
        ]
    },
    "@I2@": {
        "ID": "@I2@",
        "NAME": "John /Smith/",
        "SEX": "M",
        "BIRT": "8 APR 1946",
        "DEAT": "N/A",
        "HUSB": [
            "@F1@"
        ]
    }
}
```

### Families:

```json
{
    "@F1@": {
        "ID": "@F1@",
        "HUSB": "@I2@",
        "WIFE": "@I1@",
        "CHIL": [
            "@I3@",
            "@I5@"
        ],
        "DIV": "N/A",
        "MARR": "N/A"
    },
    "@F2@": {
        "ID": "@F2@",
        "HUSB": "@I4@",
        "WIFE": "@I3@",
        "CHIL": [
            "@I7@"
        ],
        "DIV": "N/A",
        "MARR": "N/A"
    }
}
```