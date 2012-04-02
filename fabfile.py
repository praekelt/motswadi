from fabric.api import cd, prefix, run, sudo

def restart():
    sudo('/etc/init.d/nginx restart')
    sudo('supervisorctl reload')

def provision():
    sudo('apt-get update')
    sudo('apt-get install -y git-core puppet')
    run('git clone https://github.com/praekelt/motswadi.git')
    with cd('motswadi'):
        sudo('puppet ./manifests/motswadi.pp --modulepath ./manifests/modules')
    with cd('/var/praekelt/motswadi'):
        with prefix('. ve/bin/activate'):
            sudo('./motswadi/manage.py syncdb')
            sudo('./motswadi/manage.py migrate')
            sudo('./motswadi/manage.py collectstatic')
    restart()
    run('rm -rf ~/motswadi')
