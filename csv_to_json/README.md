# Introduction
This script converts a CSV file into a custom json format


### Using the Tool
To use the script, import the function in the following format:

```
$ csv_to_json(file_path, save_path, json_structure, indent, delimiter)
```

- **file_path**: this is the path to your csv file
- **save_path**: this is the new file path to save (xx.json)
- **json_structure**: this is used to specify how you want the json file to be formatted. For more, read the next section. If you do not specify, by default it dumps a json file with column labels (assumption: first row are labels) as key, and column data as values.
- **indent**: The indentation for json file. By default, it indents json file by 4 spaces for easy read. If you specify None, it will not indent anything.
- **delimiter**: the delimiter of how your data columns are separated. By default, it assumes csv file uses "," as delimiter.

### Json Structure Format

By default, if you do not specify this parameter, it dumps a json file with column labels (assumption: first row are labels) as key, and column data as values.

If you want to customize the json structure, pass a dictionary in the following format, depending on your goal:

**Note: the `key_label` and `data_column_name` has to match exactly with the names in csv file!**

- You want to format each ROW of the csv file

```
{
    "key_label": [
        "data_column_name_1",
        {
            "sub_key_label": "data_column_name_2" 
            ...
        },
        ...
    ],
}
```

In the above format, it uses the value at `key_label` column of each row as the json key for that row, and recursively format the sub_structure of the json file, where values are value at `data_column_name_x` column of that row.

- You want to format each COLUMN of the csv file

```
{
    "key_label_1": [
        "data_column_name_1",
        {
            "sub_key_label": "data_column_name_2"
            ...
        },
        ...
    ],
    "key_label_2": [
        "data_column_name_3", 
        {
            "sub_key_label": "data_column_name_2"
            ...
        },
        ...
    ],
}
```

In the above format, it uses `key_label_x` LITERALLY as the json key, and recursively format the sub_structure of the json file, where values are ALL the column data for `data_column_name_x` column.

#### Examples

Say, you have a csv file like so:

First Name | Last Name | Email Address| Phone Number
--- | --- | --- | ---
Alex  | Wong | example@gmail.com | 111-222-333
Alice  | Andressen | example@domain.com  | 444-555-666

* Using json structure 1:

```
{
    "First Name": {
        "Last Name": "Last Name",
        "Contact Information": {
            "Email": "Email Address",
            "Phone": "Phone Number"
        }
    }
}
```

will return the following json file:

```
{
    "Alex": {
        "Last Name": "Wong",
        "Contact Information": {
            "Email": "example@gmail.com",
            "Phone": "111-222-333"
        }
    },
    "Alice": {
        "Last Name": "Andressen",
        "Contact Information": {
            "Email": "example@domain.com",
            "Phone": "444-555-666"
        }
    }
}
```

* Using json structure 2:

```
{
    "Name": {
        "First Names": "First Name",
        "Last Names": "Last Name"
    },
    "Email List": "Email Address",
    "Phones": "Phone Number"
}
```

will return the following json file:

```
{
    "Name": {
        "First Names": [
            "Alex",
            "Alice"
        ],
        "Last Names": [
            "Wong",
            "Andressen"
        ]
    },
    "Email List": [
        "example@gmail.com",
        "example@domain.com"
    ],
    "Phones": [
        "111-222-333",
        "444-555-666"
    ]
}
```


# Software
You need Python (2/3).
