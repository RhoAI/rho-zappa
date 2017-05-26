import os
import sys
import argparse
from jinja2 import Template, FileSystemLoader, Environment


def extract_env_variables(filename):
    """ Extract env variables from .env file and return as list of tuples.
    """
    env_tuples = []
    for env_line in open(os.path.abspath(filename)):
        env_line = env_line.strip()
        (key, val) = env_line.split('=')
        env_tuples.append((key, val))

    return env_tuples


def generate_command(deploy_cmd, deploy_env):
    """ Validate the command and destination envirionments, generate zappa cmd
    """
    available_commands = ('deploy', 'undeploy', 'update')
    available_environments = ('dev', 'dev2', 'stag', 'prod')
    if deploy_cmd not in available_commands\
            or deploy_env not in available_environments:
        print("Must provide command {0} and environment {1}"
              .format(available_commands, available_environments))
        exit()
    return "zappa" + " " + deploy_cmd + " " + deploy_env


def render_settings_file(env_tuples, template_filename):
    """ Render our settings file for zappa with env variables.
    """
    # Generate our zappa_settings.json with secrets as environment variables.
    # We do this on the fly so that we don't track our env variables.
    template_dir = os.path.dirname(template_filename)
    template_filename = os.path.basename(template_filename)
    env = Environment(loader=FileSystemLoader(template_dir))
    template = env.get_template(template_filename)
    rendered_settings = template.render(env_tuples=env_tuples)

    with open(template_dir + 'zappa_settings.json', 'w') as fh:
        fh.write(rendered_settings)

    return True


def main():
    parser = argparse.ArgumentParser(description='Deploy a zappa app.')
    parser.add_argument('--env', type=str,
                        help='Environment file name.')
    parser.add_argument('--cmd', type=str,
                        help='Zappa Command to run.')
    parser.add_argument('--dest', type=str,
                        help='Destination Zappa environment.')
    parser.add_argument('--template', type=str, default='zappa_settings.j2',
                        help='Zappa settings template file.')

    args = parser.parse_args()

    env_tuples = extract_env_variables(args.env)
    zappa_command = generate_command(args.cmd, args.dest)
    rendered = render_settings_file(env_tuples, args.template)

    if rendered:
        os.system(zappa_command)


if __name__ == '__main__':
    main()
