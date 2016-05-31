# Ansible playbook for Uberspace

This playbook helps you set up and manage your Uberspace(s).

It configures a few common things that I find essential for Uberspaces and it is extensible for other stuff.

## Current features

- [Let's Encrypt SSL certificates](https://wiki.uberspace.de/webserver:https#let_s-encrypt-zertifikate)
- [WordPress](https://wordpress.org/) using the awesome [Bedrock](https://roots.io/bedrock/) boilerplate

## Requirements

- An Uberspace, get one at [uberspace.de](https://uberspace.de)
- Ansible

## Usage

1. Copy `uberspaces.example` to `uberspaces` and add your Uberspace host(s) and username(s)
2. Copy `host_vars/UBERSPACE_NAME.UBERSPACE_HOST.uberspace.de.example` to a new file named without the `.example` suffix and replace `UBERSPACE_NAME` with your username, e.g. `julia` and `UBERSPACE_HOST` with your Uberspace host, e.g. `eridanus`.
3. Add the domains you'd like to run on the respective Uberspace to the file created in step 2.
4. Repeat steps 2 and 3 for all your Uberspaces.
5. Run the playbook using `ansible-playbook --ask-pass site.yml`.
6. Enjoy!

If you have an SSH keypair and your public key is installed in `~/.ssh/id_rsa.pub` on your local computer, the key will be stored in `~/.ssh/authorized_keys` on your Uberspace and you won't need the `--ask-pass` argument in subsequent runs.

### Let's Encrypt

Nothing to do or configure here. This works automagically for all your domains.

### WordPress

1. To setup a WordPress instance, simply create an entry under `wordpress_instances` in your `host_vars` file (see `host_vars/UBERSPACE_NAME.UBERSPACE_HOST.uberspace.de.example` for an example)
2. Use the default `bedrock_repo` from `https://github.com/roots/bedrock.git` or use your own forked repo of the boilerplate (make sure your Uberspace can access your Git host in that case)
3. Add the domains through which your WordPress should be accessible
4. Make sure to add these domains to the top-level `domains` section in the `host_vars` file as well!

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

[I](http://jan.sh) built this. By myself. On my computer.
