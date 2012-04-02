from fabric.api import cd, prefix, run, sudo

def restart():
    sudo('/etc/init.d/nginx restart')
    sudo('supervisorctl reload')

def provision():
    sudo('apt-get update')
    sudo('apt-get install -y git-core puppet')
    run('rm -rf ~/motswadi')
    run('git clone https://github.com/praekelt/motswadi.git')
    with cd('motswadi'):
        sudo('puppet ./manifests/motswadi.pp --modulepath ./manifests/modules')
    with cd('/var/praekelt/motswadi'):
        with prefix('. ve/bin/activate'):
            sudo('./motswadi/manage.py syncdb', user="ubuntu")
            sudo('./motswadi/manage.py migrate', user="ubuntu")
            sudo('./motswadi/manage.py collectstatic', user="ubuntu")
    restart()
    run('rm -rf ~/motswadi')

def release():
    with cd('/var/praekelt/motswadi'):
        sudo('git pull origin master', user='ubuntu')
        with prefix('. ve/bin/activate'):
            sudo('./motswadi/manage.py syncdb', user="ubuntu")
            sudo('./motswadi/manage.py migrate', user="ubuntu")
            sudo('./motswadi/manage.py collectstatic', user="ubuntu")
    restart()
