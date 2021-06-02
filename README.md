# Ansible playbook for Uberspace

This playbook helps you set up and manage your Uberspace(s).

## Current features

- Registering domains for web and mail, and optionally symlinking docroot to the home directory
- [WordPress](https://wordpress.org/) using the [Bedrock](https://roots.io/bedrock/) boilerplate

## Requirements

- An Uberspace, get one at [uberspace.de](https://uberspace.de)
- Ansible

## Usage

1. Copy `uberspaces.example` to `uberspaces` and add your Uberspace host(s) and username(s)
2. Copy `site.yml.example` to `site.yml` or any other playbook name you want and start adapting it to your needs
3. The `uberspace` role handles uploading local ssh keys, generating a key for the managed machine and registering domains for web or mail against the uberspace host with an optional symlink to home
4. The `uberspace_wordpress_bedrock` role installs wordpress bedrock, creating the database for it and linking the docroot of the instance to the specified entry points

#### Bonus: Deploy hooks

Normally, your WordPress instances will be updated from your repo daily via a cron job. However, if you want to deploy your WordPress whenever your repository changes, you can specify a value for the optional `webhook_key` in each of your WordPress configs.

With a `webhook_key` defined, you will be able to create a post-receive hook on your Git server or use your Uberspace as a webhook URL on repository hosting services such as [Planio](https://plan.io/subversion-hosting-and-git-hosting/).

Your webhook URLs will be composed like this:

```
https://{{ uberspace name }}.{{ uberspace host }}.uberspace.de/cgi-bin/wordpress-update-{{ wordpress instance name }}.cgi?{{ wordpress instance webhook key }}
```

A simple post-receive hook on your Git server could look like this, it would have to go in `hooks/post-receive`:

```bash
#!/bin/sh
curl -s 'https://julia.eridanus.uberspace.de/cgi-bin/wordpress-update-example_blog.cgi?secretsauce123'
```

Or if you use [Planio](https://plan.io), simply enter your URL via **Settings** &rarr; **Repositories** &rarr; *your repo* &rarr; **Edit** &rarr; **Post-Receive webhook URL**

## License

MIT.

## Contributing

To contribute something you usually configure on your Uberspace, please fork this repo, create a new role (or add to an existing one if it makes sense) and submit a pull request.

## Credits

[Jan](http://jan.sh) built this. By himself. On his computer.

Then U7 came along with breaking changes and Peter Nerlich eventually tried to rewrite this for the new version. Though in the process, he self righteously changed stuff he deemed weird and removed some features he didn't use himself, completely destroying any backwards compatibility.
