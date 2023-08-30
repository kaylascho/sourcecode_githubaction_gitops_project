import os
import requests
import subprocess
import yaml
import shutil

print("VALUE_TO_UPDATE:", os.environ.get('VALUE_TO_UPDATE'))
print("PROPERTY_PATH:", os.environ.get('PROPERTY_PATH'))
print("GITHUB_TOKEN:", os.environ.get('GITHUB_TOKEN'))


def main():
    # Input values from environment variables
    value_to_update = os.environ.get('VALUE_TO_UPDATE')
    property_path = os.environ.get('PROPERTY_PATH')
    github_token = os.environ.get('GITHUB_TOKEN')

    if None in [value_to_update, property_path, github_token]:
        print("One or more required environment variables not found.")
        return

    print("Available environment variables:", os.environ.keys())

    # Remove 'gitops_project' directory if it exists
    if os.path.exists('gitops_project'):
        shutil.rmtree('gitops_project')

    # Update values.yaml in the gitops_project
    update_values_yaml(value_to_update, property_path, github_token)

def update_values_yaml(new_value, property_path, github_token):
    # Clone the gitops_project repository
    try:
        #subprocess.run(['git', 'clone', '--depth', '1', 'https://github.com/kaylascho/gitops_project.git', 'gitops_project'])
        #os.chdir('gitops_project')

        repository_url = f"https://github.com/kaylascho/gitops_project.git"
        subprocess.run(['git', 'clone', '--depth', '1', repository_url, 'gitops_project'])
        os.chdir('gitops_project')


        # Read and update values.yaml
        values_path = 'k8s/springapp/values.yaml'
        with open(values_path, 'r') as file:
            data = yaml.safe_load(file)
        nested_keys = property_path.split('.')
        target = data
        for key in nested_keys[:-1]:
            target = target[key]
        target[nested_keys[-1]] = new_value
        with open(values_path, 'w') as file:
            yaml.dump(data, file)

        # Verify current working directory
        print("Current Working Directory:", os.getcwd())
        print("Repository URL:", "https://github.com/kaylascho/gitops_project.git")

        # Configure Git user identity (author) for this commit
        subprocess.run(['git', 'config', 'user.email', 'orimoloyekayode@yahoo.com'])
        subprocess.run(['git', 'config', 'user.name', 'kaylascho'])

        # Add, commit, and push changes to gitops_project
        subprocess.run(['git', 'add', values_path])
        subprocess.run(['git', 'commit', '-m', 'Update values.yaml: Description of changes'])
        subprocess.run(['git', 'push', 'origin', 'master'])

    except Exception as e:
        import traceback
        print("An error occurred:", e)
        traceback.print_exc()  # Print the full traceback
        print("Changes were not applied.")

    # Print action's output to understand its behavior
    log_file_path = os.path.join(os.environ['GITHUB_WORKSPACE'], 'yaml-update-action.log')

    with open(log_file_path, 'w') as log_file:
        log_file.write("The update_yaml.py script was executed successfully.")

if __name__ == "__main__":
    main()
