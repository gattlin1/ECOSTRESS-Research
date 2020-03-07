def make_nasa_dataset(file_path):
    dataset = []
    with open(file_path, 'r', errors='ignore') as file:
        for line in file.readlines():
            if line.count(':') == 0 and line != '\n' and line != '\t\n':
                line = line.replace(' ', '').strip('\n').split('\t')
                line[0] = float(line[0])
                line[1] = float(line[1])
                dataset.append([line[0], line[1]])

    return dataset

