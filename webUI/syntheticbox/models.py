import json
import numpy as np
import pandas as pd


def save_uploaded_file(f, current_file):
    with open(current_file + ".csv", 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)


def save_joined_file(f, current_file):
    f.to_csv(current_file + '.csv', index=False)


def in_memory_files_to_csv(in_memory_files):
    csv_files = []
    for in_memory_file in in_memory_files:
        csv = pd.read_csv(in_memory_file.file)
        csv_files.append(csv)
    return csv_files


def join_files(csv_files, join_column):
    merged = csv_files[0]
    for file in csv_files[1:]:
        merged = merged.merge(file, how='inner', on=join_column)
    return merged


def chart_position_score(current_file):
    data = pd.read_csv(current_file)
    return_data = {'datapoint': [], 'top10': [], 'overall': []}
    score_value = data["Score"].tolist()
    position_value = [x for x in range(1, len(data) + 1)]
    for i in range(len(score_value)):
        return_data['datapoint'].append([position_value[i], score_value[i]])
    # get the median data
    attr_list = []
    for i in range(2, data.shape[1] - 1):
        attr_list.append(data.iloc[:, i].tolist())
    #####################
    colname = data.columns[2:5]
    topTen = 10
    for i in range(len(attr_list)):
        return_data['top10'].append(
            [colname[i], max(attr_list[i][0:topTen]), np.median(attr_list[i][0:topTen]), min(attr_list[i][0:topTen])])
        return_data['overall'].append([colname[i], max(attr_list[i]), np.median(attr_list[i]), min(attr_list[i])])
    return return_data


def save_file_to_server(file_name, data, ext='.txt'):
    with open(file_name + ext, 'w') as outfile:
        outfile.write(str(data))
    outfile.close()


def get_json_from_file(file_name):
    with open(file_name, 'r') as myfile:
        json_data = myfile.read().replace('\n', '')
    return json_data


def getSizeOfDataset(current_file):
    data = pd.read_csv(current_file + ".csv")
    return len(data)


class DataAnalyzerUI(object):
    def __init__(self, threshold_size=100):
        self.threshold_size = threshold_size
        self.dataset_description = {}
        self.input_dataset = None
        self.display_dataset = None
        self.json_data = {}

    def read_dataset_from_csv(self, file_name=None):
        file_name = file_name + ".csv"
        try:
            self.input_dataset = pd.read_csv(file_name)
        except (UnicodeDecodeError, NameError):
            self.input_dataset = pd.read_csv(file_name, encoding='latin1')

        num_tuples, num_attributes = self.input_dataset.shape
        if num_tuples > self.threshold_size:
            self.display_dataset = self.input_dataset.head(self.threshold_size)
        else:
            self.display_dataset = self.input_dataset

    def get_dataset_meta_info(self):
        num_tuples, num_attributes = self.input_dataset.shape
        attribute_list = self.input_dataset.columns.tolist()

        meta_info = {"num_tuples": num_tuples, "num_attributes": num_attributes, "attribute_list": attribute_list}
        self.dataset_description['meta'] = meta_info

    def get_json_data(self):
        self.json_data = self.display_dataset.to_json(orient='records')

    def save_dataset_description_to_file(self, file_name):
        with open(file_name, 'w') as outfile:
            json.dump(self.dataset_description, outfile, indent=4)

    def save_dataset_to_file(self, file_name):
        with open(file_name, 'w') as outfile:
            outfile.write(str(self.json_data))

    def display_dataset_description(self):
        print(json.dumps(self.dataset_description, indent=4))
