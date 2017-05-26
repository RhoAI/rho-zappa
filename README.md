# Rho Zappa

Simple wrapper for [Zappa](https://www.zappa.io/) that allows you to use `*.j2`
templates for your `zappa_settings.json` file. This allows you to do things
such as include environment variables in your Lambda deployment without
tracking them in your repository.

__Note:__ This is extremely limited at the moment, it only supports the ability
to add environment variables. Future options will be added as necessary / PRs
welcome.

## Setup

* Full instructions on using Zappa here:
[https://github.com/Miserlou/Zappa](https://github.com/Miserlou/Zappa)
* Create a `zappa_settings.j2` file in your repository in place of your
`zappa_settings.json` file.
* Add whatever logic you want in the
[jinja2 template](http://jinja.pocoo.org/docs/2.9/) (example below)
* Run command through Rho Zappa instead of directly to Zappa. e.g.
`rho-zappa --env .env.atla-vista-dev01 --cmd update --dest dev` instead of
`zappa update dev`

## Example Template
```
{
    "dev": {
        "project_name": "my-awesome-project",
        "app_function": "my_awesome_project.app.app",
        "profile_name": "my_awesome_zappa_user",
        "s3_bucket": "my_awesome_s3_bucket",
        "api_key_required": true,
        "environment_variables": {
        {% for env_tuple in env_tuples -%}
          "{{env_tuple[0]}}": "{{env_tuple[1]}}"{{ "," if not loop.last }}
        {% endfor %} }
    }
}
```
