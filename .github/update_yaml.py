import os
import subprocess
import yaml
import shutil

def main():
    # Input values from environment variables
    value_to_update = os.environ.get('VALUE_TO_UPDATE')
    property_path = os.environ.get('PROPERTY_PATH')
    github_token = os.environ.get('GITHUB_TOKEN')

    if None in [value_to_update, property_path, github_token]:
        print("One or more required environment variables not found.")
        return

    print("Available environment variables:", os.environ.keys())

    # Remove 'manifest_githubaction_gitops_project' directory if it exists
    if os.path.exists('manifest_githubaction_gitops_project'):
        shutil.rmtree('manifest_githubaction_gitops_project')

    # Update values.yaml in the manifest_githubaction_gitops_project
    update_values_yaml(value_to_update, property_path, github_token)

def update_values_yaml(new_value, property_path, github_token):
    # Clone the manifest_githubaction_gitops_project repository
    try:
        repository_url = f"https://{github_token}@github.com/kaylascho/manifest_githubaction_gitops_project.git"
        subprocess.run(['git', 'clone', '--depth', '1', repository_url, 'manifest_githubaction_gitops_project'])
        os.chdir('manifest_githubaction_gitops_project')

        # Update the tag value in values.yaml
        values_path = 'k8s/springapp/values.yaml'
        with open(values_path, 'r') as file:
            lines = file.readlines()
        with open(values_path, 'w') as file:
            for line in lines:
                if line.strip().startswith('tag:'):
                    file.write(f'  tag: "{new_value}"\n')
                else:
                    file.write(line)

        # Verify current working directory and repository URL
        print("Current Working Directory:", os.getcwd())
        print("Repository URL:", repository_url)

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

# source code repo name is https://github.com/kaylascho/sourcecode_githubaction_gitops_project
# Manifest files repo name is https://github.com/kaylascho/manifest_githubaction_gitops_project