anaconda = {
    'conda_env_create':'conda create -n yourenvname python=x.x anaconda',
    'conda_env_activate': 'source activate yourenvname',
    'conda_env_install_pkg': 'conda install -n yourenvname [package]',
    'conda_env_remove' : 'conda remove -n yourenvname -all',
    'conda_env_create_requirements': 'conda list -e > requirements.txt',
    'conda_env_create_env_with_requirements': ' conda create --name <environment_name> --file requirements.txt',
    'conda_env_install_requirements' : 'conda install --file requirements.txt',
}