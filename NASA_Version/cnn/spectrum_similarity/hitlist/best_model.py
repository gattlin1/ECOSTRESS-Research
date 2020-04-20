import os

def get_best_model_at_level(level, results):
    results.sort(key=lambda x: x[1][level], reverse=True)
    return results[0]

if __name__=='__main__':
    results_dir = 'results/non-nlc/'
    model_results = []
    for results in os.listdir(results_dir):
        model_path = os.path.join(results_dir, results)
        with open(model_path, 'r') as file:
            content = file.read()
            index = content.index('Calculcated Best Matches')
            content = content[index:].split('\n')
            level_acc = [x.split(':')[-1] for x in content]

            model = [results, level_acc]
            model_results.append(model)
    for i in range(4):
        best_model_at_i = get_best_model_at_level(i, model_results)
        print(f'Best Model at Level {i + 1}')
        print(f'Name: {best_model_at_i[0]}')
        print(f'Results: {best_model_at_i[1]}')