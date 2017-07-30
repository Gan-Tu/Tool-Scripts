import csv
import json

def csv_to_json(file_path, save_path, json_structure, indent=4, delimiter=','):

    def save_json(save_path, jsonfile):
        assert type(jsonfile) == str, "invalid json file type"
        if ".json" not in save_path:
            save_path = save_path + ".json"
        try:
            with open(save_path, "w") as file:
                file.write(jsonfile)
            print("Successfully saved at", save_path)
        except Exception as e:
            print("Failed to save. Error:", e)

    def load_csv(file_path, delimiter=','):
        try:
            if '.csv' not in file_path:
                file_path = file_path + '.csv'
            with open(file_path, 'r') as csvfile:
                reader = csv.reader(csvfile, delimiter=delimiter)
                data = list()
                for row in reader:
                    data.append(row)
            return data
        except Exception as e:
            print("Failed to load csv. Error:", e)

    def convert(data, json_structure, indent=4):
        try:
            print("Assuming first row are labels, processing...")
            labels = data[0]
            index_to_label = { i: label.strip() if label.strip() != '' else 'column_' + str(i) for i, label in enumerate(labels) }

            if json_structure != 'column' and len(list(json_structure.keys())) == 1:
                label_to_index = { label.strip() if label.strip() != '' else 'column_' + str(i): i for i, label in enumerate(labels) }
                primary_data_cell_key = list(json_structure.keys())[0]
                def recursive_structure(structure, data_row):
                    parsed = dict()
                    for i, label in enumerate(structure):
                        if label in parsed:
                            raise KeyError("cannot have duplicated labels in json structures: ", label)
                        nested_sub_structure = structure[label]
                        if isinstance(type(nested_sub_structure), (int, float)):
                            nested_sub_structure = str(nested_sub_structure)
                        if type(nested_sub_structure) == dict:
                            content = recursive_structure(nested_sub_structure, data_row)
                        elif type(nested_sub_structure) == str:
                            content = data_row[label_to_index[nested_sub_structure]]
                        else:
                            raise KeyError("incorrect sub_structure_label", 
                                    nested_sub_structure)
                        parsed[label] = content
                    return parsed
                result = dict()
                for row in data[1:]:
                    sub_data = recursive_structure(json_structure, row)
                    sub_data[row[label_to_index[primary_data_cell_key]]] = sub_data.pop(primary_data_cell_key)
                    result.update(sub_data)
                return json.dumps(result, indent=indent)

            else:   
                label_to_column = { 
                    label.strip() if label.strip() != '' else 'column_' + str(i): list() 
                        for i, label in enumerate(labels) 
                }
                for row in data[1:]:
                    for i, d in enumerate(row):
                        label_to_column[index_to_label[i]].append(d)
                if json_structure == 'column':
                    return json.dumps(label_to_column, indent=indent)
                else:
                    def recursive_structure(structure):
                        parsed = dict()
                        for label in structure:
                            if label in parsed:
                                raise KeyError("cannot have duplicated labels in json structures: ", label)
                                return None
                            nested_sub_structure = structure[label]
                            if isinstance(type(nested_sub_structure), (int, float)):
                                nested_sub_structure = str(nested_sub_structure)
                            if type(nested_sub_structure) == dict:
                                content = recursive_structure(nested_sub_structure)
                            elif type(nested_sub_structure) == str:
                                content = label_to_column[nested_sub_structure]
                            else:
                                raise KeyError("incorrect sub_structure_label", nested_sub_structure)
                            parsed[label] = content
                        return parsed
                    return json.dumps(recursive_structure(json_structure), indent=indent)

    data = load_csv(file_path, delimiter)

    if len(json_structure) >= 4:
        if 'row' in json_structure[:4]:
            primary_key = json_structure[4:].strip()
            if len(primary_key) <= 0:
                raise KeyError("wrong primary key for row type", primary_key)
            row_column_json = {primary_key: {x : x for x in data[0]}}
            json_structure = row_column_json

    j = convert(data, json_structure, indent)
    save_json(save_path, j)


