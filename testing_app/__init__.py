import json
import random
import docker
import github
import requests
from flask import Flask, request, jsonify
from jinja2 import Environment, PackageLoader
import testing_app.instances as instances
import testing_app.settings as settings


def create_app():
    app = Flask(__name__)
    jinja_env = Environment(loader=PackageLoader('testing_app', 'templates'))
    docker_client = docker.from_env()
    instances_repo = instances.RunningInstancesRepository()
    github_client = github.Github(settings.GITHUB_ACCESS_TOKEN)

    def get_repo_config_from_template(template_name, data):
        template = jinja_env.get_template(f'{template_name}.jinja2')
        return json.loads(template.render(**data))

    def get_repo_config(repo_name):
        used_ports = set(instances_repo.get_running_ports())
        available_ports = list(set(range(50000, 51000)) - used_ports)
        data = {'random_port': random.choice(available_ports)}
        return get_repo_config_from_template(repo_name, data)

    def start_container(image_name, run_config, port_number):
        docker_client.images.pull(image_name)
        container = docker_client.containers.run(
            image_name, detach=True, **run_config
        )
        instances_repo.set_instance(
            image_name, container.id, port_number
        )

    def kill_container(image_name):
        instance_info = instances_repo.get_instance(image_name)
        if instance_info:
            try:
                container = docker_client.containers.get(
                    instance_info['container_id']
                )
                container.stop()
                container.remove()
            except docker.errors.NotFound:
                pass
            finally:
                instances_repo.remove_instance(image_name)

    def comment_on_pull_request(repo_full_name, branch_name, config):
        repo = github_client.get_repo(repo_full_name)
        if repo:
            pulls_list = repo.get_pulls(state='open', head=branch_name)
            pr = next(iter(pulls_list), None)
            if pr:
                pr.create_issue_comment(
                    "You can test this feature at " +
                    f"{settings.SERVER_URL}:{config['port_number']}"
                )

    @app.route('/')
    def hello_world():
        return 'Hey, we have Python in a Docker container!'

    @app.route('/webhook/github', methods=['POST'])
    def github_webhook():
        github_event = request.headers.get('X-GitHub-Event')
        ref_type = request.json['ref_type']

        if (github_event == 'delete' and ref_type == 'branch'):
            branch_name = request.json['ref']

            if branch_name.startswith('feature/'):
                repository_name = request.json['repository']['name']
                repo_config = get_repo_config(repository_name)
                image_full_name = repo_config['image_full_name']
                image_tag = branch_name.replace('/', '-')
                image_name = f"{image_full_name}:{image_tag}"
                kill_container(image_name)

        return jsonify({})

    @app.route('/webhook/dockerhub', methods=['POST'])
    def docker_hub_webhook():
        image_tag = request.json.get('push_data', {}).get('tag')
        if image_tag and image_tag.startswith('feature-'):
            repository_name = request.json['repository']['name']
            repo_config = get_repo_config(repository_name)
            image_full_name = repo_config['image_full_name']
            image_name = f"{image_full_name}:{image_tag}"
            kill_container(image_name)
            start_container(
                image_name,
                repo_config['run_config'],
                repo_config['port_number']
            )

            # Send callback to Docker Hub
            callback_url = request.json['callback_url']
            requests.post(callback_url, json={'state': 'success'})

            repository_full_name = repo_config['repository_full_name']
            branch_name = image_tag.replace('feature-', 'feature/')
            comment_on_pull_request(
                repository_full_name, branch_name, repo_config
            )

        return jsonify({})

    return app
